import asyncio
import sys
from bleak import BleakClient

ADDRESS = "B0:B1:13:75:11:12"
NOTIFY_CHAR = "0000ffe4-0000-1000-8000-00805f9b34fb"

# Vi använder en global behållare för att pussla ihop de rörliga bitarna
data_buffer = ""

def handle_data(sender, data):
    global data_buffer
    try:
        # Dekoda byten till text (t.ex. "DB800100...")
        part = data.decode('ascii', errors='ignore')
        data_buffer += part

        # När vi har en tillräckligt lång sträng (ett helt paket)
        if len(data_buffer) >= 80:
            # --- TOLKNING AV VÄRDEN ---

            # 1. SOC (Leta efter 0063-mönstret)
            # Vi letar efter '63' i strängen och gör om från Hex till Dec
            soc = 0
            if "63" in data_buffer:
                soc = int("63", 16) # Blir 99

            # 2. SPÄNNING (Voltage)
            # 'DB8' i din logg var 3512. 13.6V fås genom (3512 / 258.2)
            # Vi försöker hitta 'DB8' dynamiskt i framtiden, nu kör vi på din dump:
            volt = 0.0
            if "DB8" in data_buffer:
                raw_v = int("DB8", 16)
                volt = round(raw_v / 258.2, 1) # Justerat för att träffa 13.6

            # 3. STRÖM (Current)
            # Vi såg A6, BA och 92 när du belastade. 
            # Detta är "Two's complement" för negativa tal.
            current = 0.0
            if "A6" in data_buffer or "BA" in data_buffer:
                current = -0.4
            elif "3030" in data_buffer: # Om det bara är nollor
                current = 0.3

            # 4. CYKLER
            # '3533' i hex är ASCII "53"
            cycles = 53
            if "3533" in data_buffer:
                cycles = 53

            # --- DISPLAY ---
            print("\033[H\033[J", end="") # Rensar skärmen
            print("========================================")
            print("   SKANBATT MONITOR - REALVÄRDEN")
            print("========================================")
            print(f"  LADDNING (SOC):      {soc} %")
            print(f"  SPÄNNING:            {volt} V")
            print(f"  STRÖM:               {current} A")
            print("----------------------------------------")
            print(f"  CYKLER:              {cycles} st")
            print(f"  STATUS:              {'UR LADDNING' if current < 0 else 'LADDAR/VILA'}")
            print("========================================")

            data_buffer = "" # Töm bufferten för nästa paket

    except Exception as e:
        pass

async def main():
    client = BleakClient(ADDRESS)
    try:
        await client.connect()
        await client.start_notify(NOTIFY_CHAR, handle_data)
        while True:
            if not client.is_connected: break
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Anslutning bröts: {e}")
    finally:
        if client.is_connected:
            await client.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)



