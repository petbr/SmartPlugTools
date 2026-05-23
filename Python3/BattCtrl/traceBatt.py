import asyncio
import logging
import traceback
from bleak import BleakClient

# --- INSTÄLLNINGAR ---
import asyncio
import logging
import traceback
from bleak import BleakClient

# --- INSTÄLLNINGAR ---
BMS_ADDRESS = "B0:B1:13:75:11:12"

logging.basicConfig(level=logging.INFO)

async def main():
    print(f"--- Försöker ansluta till {BMS_ADDRESS} ---")
    
    try:
        # I moderna Bleak sköts "service discovery" automatiskt vid anslutning
        async with BleakClient(BMS_ADDRESS, timeout=20.0) as client:
            print(f"Ansluten: {client.is_connected}")
            
            # Här använder vi den nya egenskapen .services (utan parenteser och utan await)
            print("\nHittade följande tjänster (Services):")
            for service in client.services:
                print(f"Service UUID: {service.uuid}")
                for char in service.characteristics:
                    print(f"  -> Karaktäristik: {char.uuid} (Properties: {char.properties})")

    except Exception as e:
        print("\n--- DETALJERAT FEL ---")
        traceback.print_exc()
        print("----------------------\n")

if __name__ == "__main__":
    asyncio.run(main())

