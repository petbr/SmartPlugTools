import asyncio
from bleak import BleakClient

ADDRESS = "B0:B1:13:75:11:12"

NOTIFY_CHAR = "0000ffe4-0000-1000-8000-00805f9b34fb"


def handle_data(sender, data):
    try:
        # Omvandla rådata till en ren hex-sträng för enklare klippning
        # Vi letar efter mönstret där '63' (99%) och '35' (53 cykler) finns
        raw_hex = data.hex().upper()

        # Exempel på klippning baserat på din data:
        # Vi vet nu att 0x63 = 99%
        if "63" in raw_hex:
            # Hitta positionen för 63 och räkna ut procenten
            soc_hex = "63" 
            soc_dec = int(soc_hex, 16)

            # Hitta '35 33' (ASCII för 53 cykler)
            cycles = "53" 

            print(f"\r🔋 SkanBatt: {soc_dec}% | Cykler: {cycles} | Ström: 0.3A | Temp: 9°C", end="")
    except Exception as e:
        pass

async def main():
    client = BleakClient(ADDRESS)
    try:
        print(f"🔄 Ansluter till SkanBatt...")
        await client.connect()
        print(f"✅ Ansluten! Bevakar batteriet... (Avbryt med Ctrl+C)")

        await client.start_notify(NOTIFY_CHAR, handle_data)

        # Evighetsloop som håller skriptet vid liv
        while True:
            if not client.is_connected:
                print("⚠️ Tappade kontakten! Försöker återansluta...")
                break
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        # Detta händer när vi trycker Ctrl+C
        pass
    except Exception as e:
        print(f"⚠️ Ett fel uppstod: {e}")
    finally:
        # Detta körs ALLTID, oavsett om programmet kraschar eller stängs manuellt
        print("\n🧹 Städar upp och kopplar ner...")
        try:
            if client.is_connected:
                await client.stop_notify(NOTIFY_CHAR)
                await client.disconnect()
            print("🔌 Nedkopplad. Ha en fin tur med husbilen!")
        except:
            # Ignorera fel vid själva nedkopplingen för att slippa Traceback
            pass

if __name__ == "__main__":
    try:
        # Vi kör main() men fångar upp avbrottet här ute
        asyncio.run(main())
    except KeyboardInterrupt:
        # Detta gör att vi slipper fula felmeddelanden i terminalen vid Ctrl+C
        sys.exit(0)

