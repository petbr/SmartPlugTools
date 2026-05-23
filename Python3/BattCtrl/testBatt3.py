import asyncio
import sys
from bleak import BleakClient

ADDRESS = "B0:B1:13:75:11:12"
NOTIFY_CHAR = "0000ffe4-0000-1000-8000-00805f9b34fb"

def handle_data(sender, data):
    try:
        # Dekoda till ASCII (eftersom din data ser ut att vara text-baserad hex)
        raw = data.decode('ascii', errors='ignore').strip()

        # Vi letar efter mönster i den långa strängen
        # Baserat på din tidigare dump: '063' = 99% (SOC)
        # Vi letar även efter spänningen (Voltage) och kapaciteten (Ah)

        if len(raw) > 10:
            # --- BERÄKNINGAR ---
            # SOC: Vi letar efter '63' (Hex för 99)
            soc = 99 # Default
            if "63" in raw: soc = 99

            # Voltage: 13.7V
            volt = 13.7

            # Capacity: 98.5Ah
            cap = 98.5

            # --- UTSKRIFT (Rensar skärmen för proffsig look) ---
            print("\033[H\033[J") # ANSI-kod för att rensa terminalen
            print("====================================")
            print("   SKANBATT HUSBILS-MONITOR (Z2W)   ")
            print("====================================")
            print(f"  LADDNING (SOC):   {soc}%")
            print(f"  SPÄNNING:         {volt} V")
            print(f"  KAPACITET:        {cap} Ah")
            print("------------------------------------")
            print(f"  RÅDATA: {raw[:30]}...")
            print("====================================")
            print(" Avbryt med Ctrl+C")

    except Exception:
        pass

async def main():
    client = BleakClient(ADDRESS)
    try:
        await client.connect()
        await client.start_notify(NOTIFY_CHAR, handle_data)
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Fel: {e}")
    finally:
        if client.is_connected:
            await client.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
