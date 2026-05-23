import asyncio
from bleak import BleakClient
# Din fastställda adress
ADDRESS = "B0:B1:13:75:11:12"
# Karakteristiken som strömmar data
NOTIFY_CHAR = "0000ffe4-0000-1000-8000-00805f9b34fb"
def handle_raw_data(sender, data):
    # Vi skriver ut både som TEXT (ASCII) och som HEX-koder
    as_text = data.decode('ascii', errors='ignore').strip()
    as_hex = data.hex(' ').upper()
    print(f"HEX: {as_hex}")
    if len(as_text) > 0:
        print(f"TXT: {as_text}")
    print("-" * 30)
async def run():
    print(f"Ansluter till {ADDRESS}...")
    try:
        async with BleakClient(ADDRESS) as client:
            print("✅ Ansluten! Tänd lampan nu (väntar 20s)...")
            await client.start_notify(NOTIFY_CHAR, handle_raw_data)
            await asyncio.sleep(20)
            await client.stop_notify(NOTIFY_CHAR)
            print("Klar. Kopiera texten ovan!")
    except Exception as e:
        print(f"⚠️ Fel: {e}")
if __name__ == "__main__":
    asyncio.run(run())
