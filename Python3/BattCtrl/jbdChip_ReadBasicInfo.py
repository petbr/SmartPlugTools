import asyncio
from bleak import BleakClient, BleakScanner

# Din kända info
ADDRESS = "B0:B1:13:75:11:12"




JBD_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
BASIC_INFO_CMD = bytes.fromhex("DD A5 03 00 FF FD 77")

def notification_handler(sender, data):
    print(f"SVAR: {data.hex().upper()}")

async def run():
    print(f"Försöker ansluta till {ADDRESS}...")
    
    # 1. Hitta enheten först för att fräscha upp Bluetooth-stacken
    device = await BleakScanner.find_device_by_address(ADDRESS, timeout=10.0)
    if not device:
        print("Kunde inte hitta enheten. Kontrollera att Bluetooth är PÅ.")
        return

    try:
        # 2. Anslut med en längre timeout och utan cache
        async with BleakClient(device, timeout=20.0) as client:
            print(f"Ansluten! Signalstyrka (RSSI): {device.rssi}")
            
            # 3. Starta notifieringar
            await client.start_notify(JBD_UUID, notification_handler)
            
            # 4. Skicka kommandot (vi testar båda skrivmetoderna)
            print("Skickar kommando...")
            await client.write_gatt_char(JBD_UUID, BASIC_INFO_CMD, response=False)
            
            # Vänta på svar
            await asyncio.sleep(5.0)
            await client.stop_notify(JBD_UUID)
            
    except Exception as e:
        # repr(e) ger oss den tekniska felkoden (t.ex. [org.bluez.Error.Failed])
        print(f"Tekniskt fel: {repr(e)}")

if __name__ == "__main__":
    asyncio.run(run())

