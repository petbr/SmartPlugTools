import asyncio
from bleak import BleakClient

# --- INSTÄLLNINGAR ---
# Skriv in din adress här (från scan.py)
BMS_ADDRESS = "B0:B1:13:75:11:12" 

# JBD BMS Standard-UUIDs för läs/skriv
WRITE_UUID = "0000ff02-0000-1000-8000-00805f9b34fb"
READ_UUID  = "0000ff01-0000-1000-8000-00805f9b34fb"

# Kommandot för att hämta grundläggande info (Voltage, Current, SOC, Temp)
# Format: [Start, MsgType, Command, Length, Data, Checksum, End]
READ_INFO_CMD = bytearray([0xDD, 0xA5, 0x03, 0x00, 0xFF, 0xFD, 0x77])

def parse_bms_data(data):
    """Tolkar rådata från batteriet till läsbara värden."""
    if len(data) < 20:
        return None

    # Spänning (Voltage) - Index 4 & 5 (enhet: 10mV)
    voltage = ((data[4] << 8) | data[5]) / 100.0

    # Ström (Current) - Index 6 & 7 (enhet: 10mA, signed int)
    current_raw = (data[6] << 8) | data[7]
    if current_raw > 32767:
        current_raw -= 65536
    current = current_raw / 100.0

    # Kapacitet (State of Charge) - Index 23 (%)
    soc = data[23]

    # Temperatur - Index 27 & 28 (enhet: 0.1 Kelvin - 273.15)
    temp_raw = (data[27] << 8) | data[28]
    temp = (temp_raw - 2731) / 10.0

    return {
        "volt": voltage,
        "amp": current,
        "soc": soc,
        "temp": temp
    }

async def fetch_battery_data():
    print(f"Försöker ansluta till {BMS_ADDRESS}...")
    
    try:
        async with BleakClient(BMS_ADDRESS) as client:
            if not client.is_connected:
                print("Kunde inte etablera anslutning.")
                return

            print("Ansluten! Hämtar data...")

            # En framtida lösning kräver ofta "notifications" men för en enkel 
            # avläsning kan vi skicka kommandot och vänta på svar.
            # Vi definierar en intern funktion för att fånga svaret
            response_data = bytearray()

            def callback(sender, data):
                nonlocal response_data
                response_data.extend(data)

            await client.start_notify(READ_UUID, callback)
            await client.write_gatt_char(WRITE_UUID, READ_INFO_CMD)
            
            # Vänta en kort stund på att hela paketet ska landa
            await asyncio.sleep(1.0) 
            await client.stop_notify(READ_UUID)

            res = parse_bms_data(response_data)
            
            if res:
                print("\n" + "="*25)
                print(f" BATTERISTATUS (Skanbatt)")
                print("="*25)
                print(f"Spänning:  {res['volt']:.2f} V")
                print(f"Ström:     {res['amp']:.2f} A")
                print(f"Laddning:  {res['soc']}%")
                print(f"Temp:      {res['temp']:.1f}°C")
                print("="*25)
            else:
                print("Fick svar, men kunde inte tolka datan.")

    except Exception as e:
        print(f"Ett fel uppstod: {e}")

if __name__ == "__main__":
    asyncio.run(fetch_battery_data())
