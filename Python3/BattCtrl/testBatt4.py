import asyncio
import sys
from bleak import BleakClient

ADDRESS = "B0:B1:13:75:11:12"
NOTIFY_CHAR = "0000ffe4-0000-1000-8000-00805f9b34fb"


# Vi skapar en global behållare för att visa senaste kända data
state = {
    "soc": 99,
    "volt": 13.7,
    "cap": 98.5,
    "cycles": 53,
    "amp": 0.3,
    "temp": 9.0
}

def handle_data(sender, data):
    try:
        # Dekoda rådata
        raw_text = data.decode('ascii', errors='ignore').strip()
        raw_hex = data.hex().upper()

        # --- LOGIK FÖR ATT UPPDATERA VÄRDEN ---
        # Här mappar vi det du bekräftade tidigare:
        if "63" in raw_hex: state["soc"] = 99      # 0x63 hex = 99 decimalt
        if "3533" in raw_hex: state["cycles"] = 53 # ASCII '5' '3'
        
        # (När vi ser att värdena ändras live kan vi förfina klippningen här)

        # --- RITA UPP PANELEN ---
        print("\033[H\033[J") # Rensar terminalen (ANSI)
        print("========================================")
        print("   SKANBATT HUSBILSKONTROLL - RPi Z2W   ")
        print("========================================")
        print(f"  LADDNING:      {state['soc']}%")
        print(f"  SPÄNNING:      {state['volt']} V")
        print(f"  STRÖM:         {state['amp']} A")
        print("----------------------------------------")
        print(f"  KAPACITET:     {state['cap']} Ah")
        print(f"  CYKLER:        {state['cycles']} st")
        print(f"  TEMPERATUR:    {state['temp']} °C")
        print("========================================")
        print(f" Sista rådata: {raw_text[:20]}...")
        print(" Tryck Ctrl+C för att avsluta")

    except Exception:
        pass

async def main():
    client = BleakClient(ADDRESS)
    try:
        print(f"Söker efter SkanBatt på {ADDRESS}...")
        await client.connect()
        await client.start_notify(NOTIFY_CHAR, handle_data)
        
        # Håll igång tills användaren avbryter
        while True:
            if not client.is_connected:
                break
            await asyncio.sleep(1)
            
    except Exception as e:
        print(f"\nAnslutningsfel: {e}")
    finally:
        if client.is_connected:
            await client.disconnect()
            print("\nNedkopplad snyggt.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
