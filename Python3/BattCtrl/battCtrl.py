import asyncio
from bleak import BleakClient

# --- INSTÄLLNINGAR ---
# Ersätt med din adress från 'bluetoothctl scan on'
ADDRESS = "B0:B1:13:75:11:12"

# JBD BMS Standard-UUIDs
UART_TX_UUID = "0000ff02-0000-1000-8000-00805f9b34fb" # Skriv
UART_RX_UUID = "0000ff01-0000-1000-8000-00805f9b34fb" # Läs

# "Magic command" för att hämta basinfo (V, A, %, Temp)
QUERY_INFO = bytearray([0xDD, 0xA5, 0x03, 0x00, 0xFF, 0xFD, 0x77])

def notification_handler(sender, data):
    """Denna funktion körs när batteriet svarar."""
    # JBD skickar ett paket som börjar med 0xDD
    if data[0] == 0xDD:
        # Spänning (Voltage) finns på index 4 och 5 (enhet: 10mV)
        voltage = ((data[4] << 8) | data[5]) / 100.0
        
        # Ström (Current) finns på index 6 och 7 (enhet: 10mA)
        # OBS: Detta är ett signerat heltal (negativt vid urladdning)
        current_raw = (data[6] << 8) | data[7]
        if current_raw > 32767:
            current_raw -= 65536
        current = current_raw / 100.0
        
        # Kapacitet (%) finns på index 23
        soc = data[23]

        print("\n--- Batteristatus ---")
        print("Spänning: {} V".format(voltage))
        print("Ström:    {} A".format(current))
        print("Laddning: {} %".format(soc))
        print("---------------------")

async def run():
    print("Ansluter till Skanbatt...")
    async with BleakClient(ADDRESS) as client:
        if client.is_connected:
            print("Ansluten! Lyssnar på svar...")
            
            # Börja lyssna på svar
            await client.start_notify(UART_RX_UUID, notification_handler)
            
            # Skicka frågan till batteriet
            await client.write_gatt_char(UART_TX_UUID, QUERY_INFO)
            
            # Vänta en kort stund på att svaret ska hinna komma
            await asyncio.sleep(2.0)
            await client.stop_notify(UART_RX_UUID)
        else:
            print("Kunde inte ansluta.")

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except Exception as e:
        print("Ett fel uppstod: {}".format(e))
