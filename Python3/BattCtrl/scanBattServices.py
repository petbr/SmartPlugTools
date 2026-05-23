import asyncio
from bleak import BleakClient

# Ändra denna till din MAC-adress (viktigt: stora bokstäver och kolon)
ADDRESS = "B0:B1:13:75:11:12"

async def run():
    try:
        async with BleakClient(ADDRESS) as client:
            print(f"✅ Ansluten till {ADDRESS}")

            for service in client.services:
                print(f"\nTjänst: {service.uuid}")
                for char in service.characteristics:
                    print(f"  └─ Karakteristik: {char.uuid} | Egenskaper: {', '.join(char.properties)}")

            print("\n--- Sokning klar ---")
    except Exception as e:
        print(f"⚠️ Fel: {e}")

if __name__ == "__main__":
    asyncio.run(run())
