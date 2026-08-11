import os
import time
from datetime import datetime
import csv
import sys

TIME_ENT = 0
SOC_ENT  = 1

if len(sys.argv) > 1:
    FILE_TO_WATCH = sys.argv[1]
    print(f"Första argumentet är: {FILE_TO_WATCH}")
else:
    print("Inget argument skickades med!")
    sys.exit(1) # Avsluta skriptet om argument saknas

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
    global TIME_ENT
    global SOC_ENT
    
    print("filter_rows() STARTED")
    
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
    

def filter_rows_and_delta(allRows):
    global TIME_ENT
    global SOC_ENT
    
    print("filter_rows_and_delta() STARTED")
    print(f"TIME_ENT={TIME_ENT}, SOC_ENT={SOC_ENT} ")
    
    filteredDeltaRows = []
    lenAllRows = len(allRows)
    
    firstRow = allRows[0]
    
    firstTime = firstRow[TIME_ENT]
    firstSoc  = int(firstRow[SOC_ENT])
    firstDeltaRow = [firstTime, firstSoc, 0]
    filteredDeltaRows.append(firstDeltaRow)
    
    print("firstRow      = ", firstRow)
    print("firstTime     = ", firstTime)
    print("firstSoc      = ", firstSoc)
    print("firstDeltaRow = ", firstDeltaRow)
        
    prevSoc = firstSoc
    for curRow in allRows[1:]:
        curTime     = curRow[TIME_ENT]
        curSoc      = curRow[SOC_ENT]
        curDeltaSoc = int(curSoc) - int(prevSoc)

        curDeltaRow = [curTime, curSoc, curDeltaSoc]

        filteredDeltaRows.append(curDeltaRow)
        prevSoc = curSoc

    return filteredDeltaRows


# --- Kör funktionen ---
def runTestTiming():
    while True:
        print(f"Wait for file change: : {datetime.now().strftime('%H:%M:%S')}\n")
        wait_for_file_change(FILE_TO_WATCH)
        print(f"NO Sleep: {datetime.now().strftime('%H:%M:%S')}\n")
        #time.sleep(5.0)

    
print("Changed!")
time.sleep(1.0)
print("Fortsätter exekvering!")
lenAllRows, allRows = read_csv(FILE_TO_WATCH)
#print("rader = \n", rader)
print("#", lenAllRows)

filteredRows = filter_rows(allRows)
for row in filteredRows:
    print(row)

filteredDeltaRows = filter_rows_and_delta(filteredRows)
deltaStr = ""
for row in filteredDeltaRows:
    print(row)
    deltaStr = deltaStr + str(row) + "\n"

print(deltaStr)

with open("TestFile.txt", "w") as f:
        f.write(deltaStr)
