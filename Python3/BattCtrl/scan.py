import asyncio
from bleak import BleakScanner

async def main():
    print("Söker efter Bluetooth-enheter (som ditt batteri)...")
    try:
        # Vi letar i 5 sekunder
        devices = await BleakScanner.discover()
        if not devices:
            print("Hittade inga enheter. Är Bluetooth påslaget?")
        for d in devices:
            print(f"Hittade: {d.name} [{d.address}]")
    except Exception as e:
        print(f"Ett fel uppstod vid skanning: {e}")

if __name__ == "__main__":
    asyncio.run(main())
