from ftplib import FTP
from pathlib import Path

def kor_ftp_skript(skript_rader: list[str]):
    """Läser en array av strängar som ett skript och utför FTP-operationer."""
    
    # Variabler för att hålla sessionsinfo
    ftp_host = None
    user = None
    password = None
    kommandon = []

    # 1. Parsa skriptet (Dela upp i konfiguration och kommandon)
    for rad in skript_rader:
        rad = rad.strip()
        if not rad or rad.startswith("#"): # Hoppa över tomma rader och kommentarer
            continue
            
        if rad.lower().startswith("ftpsite:"):
            ftp_host = rad.split(":", 1)[1].strip()
        elif rad.lower().startswith("user:"):
            user = rad.split(":", 1)[1].strip()
        elif rad.lower().startswith("password:"):
            password = rad.split(":", 1)[1].strip()
        else:
            # Allt annat ses som instruktioner (LOAD, SAVE, DELETE)
            kommandon.append(rad)

    # Validering: Kontrollera att vi fick alla inloggningsuppgifter
    if not all([ftp_host, user, password]):
        print("❌ Fel: Skriptet saknar FtpSite, User eller Password.")
        return

    # 2. Starta FTP-sessionen och kör kommandona
    print(f"Ansluter till {ftp_host}...")
    try:
        with FTP(ftp_host) as ftp:
            ftp.login(user=user, passwd=password)
            print("🔑 Inloggning lyckades!")

            for kommando in kommandon:
                delar = kommando.split()
                if not delar:
                    continue
                    
                action = delar[0].upper()

                if action == "LOAD":
                    # LOAD <FtpFil> <LokalMapp>
                    if len(delar) < 3:
                        print(f"⚠️ Felaktigt LOAD-kommando: {kommando}")
                        continue
                    fjarr_fil = delar[1]
                    lokal_mapp = Path(delar[2])
                    
                    lokal_mapp.mkdir(parents=True, exist_ok=True)
                    lokal_filpath = lokal_mapp / Path(fjarr_fil).name
                    
                    print(f"📥 [LOAD] Hämtar {fjarr_fil} -> {lokal_filpath}")
                    with open(lokal_filpath, "wb") as f:
                        ftp.retrbinary(f"RETR {fjarr_fil}", f.write)

                elif action == "SAVE":
                    # SAVE <LokalFil> <FjarrMapp>
                    if len(delar) < 3:
                        print(f"⚠️ Felaktigt SAVE-kommando: {kommando}")
                        continue
                    lokal_fil = Path(delar[1])
                    fjarr_mapp = delar[2]
                    
                    if not lokal_fil.exists():
                        print(f"❌ Hittade inte lokal fil att skicka: {lokal_fil}")
                        continue
                        
                    print(f"🚀 [SAVE] Skickar {lokal_fil} -> Mapp: {fjarr_mapp}")
                    # Gå till rätt mapp på servern innan uppladdning
                    ftp.cwd(fjarr_mapp)
                    with open(lokal_fil, "rb") as f:
                        ftp.storbinary(f"STOR {lokal_fil.name}", f)
                    # Gå tillbaka till roten ifall nästa kommando körs från en annan mapp
                    ftp.cwd("/")

                elif action == "DELETE":
                    # DELETE <FtpFil>
                    if len(delar) < 2:
                        print(f"⚠️ Felaktigt DELETE-kommando: {kommando}")
                        continue
                    fjarr_fil = delar[1]
                    
                    print(f"🗑️ [DELETE] Tar bort {fjarr_fil} från servern")
                    ftp.delete(fjarr_fil)
                
                else:
                    print(f"❓ Okänt kommando ignoreras: {action}")

    except Exception as e:
        print(f"💥 Ett fel uppstod under sessionen: {e}")
    finally:
        print("🔌 Sessionen avslutad.")
