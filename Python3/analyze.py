import os
import time
import csv

FILE_TO_WATCH = "/tmp/persFile.txt"


def read_csv(in_filpath: str):
    """Läser en CSV-fil, sorterar raderna efter första kolumnen (datum/tid)

    och sparar resultatet i en ny fil.
    """
    rader = []
    print("FIX_sortera_csv_pa_datum Begin, line by line\n\n")

    # 1. Läs in filen
    with open(in_filpath, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for rad in reader:
            if rad:  # Hoppa över tomma rader
                print(rad)
                rader.append(rad)

    # 2. Sortera raderna baserat på det första elementet (index 0 = datum/tid)
    # key=lambda x: x[0] säger åt Python att titta på första kolumnen vid sortering
    rader.sort(key=lambda x: x[0])

    lenRader = len(rader)
    #print("FIX_sortera_csv_pa_datum Begin, rader, size=", lenRader, "\n")
    #print("rader[lenRader-4][0] = ", rader[lenRader-4][0])
    #print("rader[lenRader-3][0] = ", rader[lenRader-3][0])
    #print("rader[lenRader-2][0] = ", rader[lenRader-2][0])
    #print("rader[lenRader-1][0] = ", rader[lenRader-1][0])

    print("\n\nFIX_sortera_csv_pa_datum End\n\n")
    
    return lenRader, rader
    

def wait_for_file_change(file_path, poll_interval=1.0):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Filen {file_path} hittades inte.")

    # Spara nuvarande ändringstid
    last_mtime = os.path.getmtime(file_path)
    print(f"Väntar på att {file_path} ska ändras...")

    while True:
        time.sleep(poll_interval)
        try:
            current_mtime = os.path.getmtime(file_path)
            # Om ändringstiden har uppdaterats
            if current_mtime != last_mtime:
                print("Filen har ändrats!")
                break
        except FileNotFoundError:
            # Utifall filen temporärt raderas/skrivs över
            continue

def filter_rows(allRows):
    print("filter_rader() STARTED")
    SOC_ENT = 1
    
    filteredRows = []
    lenAllRows = len(allRows)
    
    firstRow = allRows[0]
    firstSoc = firstRow[SOC_ENT]
    print("firstRow=", firstRow)
    print("curSoc=", firstSoc)
        
    curSoc = firstSoc
    for curRow in allRows[1:]:
        testSoc = curRow[SOC_ENT]
        if testSoc != curSoc:    # Search for new SOC value rows
            curSoc = testSoc
            filteredRows.append(curRow)

    return filteredRows
    


# --- Kör funktionen ---
#wait_for_file_change(FILE_TO_WATCH)
print("Changed!")
time.sleep(1.0)
print("Fortsätter exekvering!")
lenAllRows, allRows = read_csv(FILE_TO_WATCH)
#print("rader = \n", rader)
print("#", lenAllRows)

filteredRows = filter_rows(allRows)
for row in filteredRows:
    print(row)



