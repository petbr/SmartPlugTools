import asyncio
from bleak import BleakClient

ADDRESS = "B0:B1:13:75:11:12"

# De troliga UUID-adresserna för SkanBatt/JBD
NOTIFY_CHARACTERISTIC = "0000ffe4-0000-1000-8000-00805f9b34fb"
WRITE_CHARACTERISTIC = "0000ffe1-0000-1000-8000-00805f9b34fb"

def notification_handler(sender, data):
    # Denna funktion körs varje gång batteriet skickar ett paket
    print(f"📥 Rådata mottagen: {data.hex(' ')}")

async def run():
    print(f"Försöker ansluta till {ADDRESS}...")
    try:
        async with BleakClient(ADDRESS) as client:
            print("✅ Ansluten!")
            
            # Starta lyssningen
            await client.start_notify(NOTIFY_CHARACTERISTIC, notification_handler)
            print(f"Prenumererar på {NOTIFY_CHARACTERISTIC}...")

            # Skicka "Status-förfrågan" (Standard JBD/SkanBatt-kommando)
            # DD A5 03 00 FF FD 77 = "Ge mig grundläggande info"
            command = bytes.fromhex("dda50300fffd77")
            print(f"📤 Skickar fråga: {command.hex(' ')}")
            await client.write_gatt_char(WRITE_CHARACTERISTIC, command)

            # Vänta 5 sekunder och se om batteriet svarar
            await asyncio.sleep(5)
            
            await client.stop_notify(NOTIFY_CHARACTERISTIC)
            print("\nTest klart.")

    except Exception as e:
        print(f"⚠️ Fel: {e}")

if __name__ == "__main__":
    asyncio.run(run())
