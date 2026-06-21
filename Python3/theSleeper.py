import time
from pathlib import Path
from datetime import datetime
from datetime import date
import asyncio
from PettraHelpers import *
from typing import NamedTuple
from jinja2 import Template

from bleak import BleakClient


# Spara starttiden direkt när programmet startar
start_tid = time.monotonic()

print(f"Programmet startade: {datetime.now().strftime('%H:%M:%S')}")

ADDRESS = "B0:B1:13:75:11:12"
NOTIFY_UUID = "0000ffe4-0000-1000-8000-00805f9b34fb"
filePath = "/tmp/theBatt.txt"
SleepTimeBetweenMeasurements = 10

requestBuffer = False    # Global flagga
newValueWasFound = False
buffer = ""

# Definiera din struct
class BattSample(NamedTuple):
    dayTime          : str
    secondsRun       : int
    cycleCounter     : int
    socStateOfCharge : int
    capacityAh       : str
    totalCapacityAh  : str
    roundedTemp      : float
    v1               : float
    v2               : float
    v3               : float
    v4               : float
    minDiffmV        : float
    maxDiffmV        : float    
    vDiffmV          : float
    thrownResults    : int

    
########################
pos_Offset       = 0
########################

StartPattern     = "800100"
thrownResults    = 0
throwLowLimit    = 2.0 # Throw when Voltage too low
callbackNr       = 0

pos_2            = 2
pos_cycleCounter = 6
pos_SOC          = 10
pos_temperature  = 14
pos_18           = 18
pos_22           = 22
pos_v1           = 26
pos_v2           = 30
pos_v3           = 34
pos_v4           = 38
pos_42           = 42
pos_44           = 46
pos_48           = 48
pos_52           = 52
pos_56           = 56

#dbgPrinting      = True
dbgPrinting      = False

NrOfMinMaxValues = 100

# Analog legacy
#bagOfMax_Analog_Values = [0]*NrOfMinMaxValues
#bagOfMin_Analog_Values = [0]*NrOfMinMaxValues

# Analog The ONE
bagOfMax_AV = [0]*NrOfMinMaxValues
bagOfMin_AV = [0]*NrOfMinMaxValues

# Normal
#bagOfMax_Digital_Values       = [0]*NrOfMinMaxValues
#bagOfMin_Digital_Values       = [0]*NrOfMinMaxValues
#bagOfMax_DigitalSigned_Values = [0]*NrOfMinMaxValues
#bagOfMin_DigitalSigned_Values = [0]*NrOfMinMaxValues


# Wrapped
#bagOfMax_WrappedDigital_Values       = [0]*NrOfMinMaxValues
#bagOfMin_WrappedDigital_Values       = [0]*NrOfMinMaxValues
#bagOfMax_WrappedDigitalSigned_Values = [0]*NrOfMinMaxValues
#bagOfMin_WrappedDigitalSigned_Values = [0]*NrOfMinMaxValues

minTemp = 999.0
maxTemp = -999.0

minSOC = 999.0
maxSOC = -999.0

minDiff_mV = 99999.0
maxDiff_mV = -99999.0

for i in range(0, NrOfMinMaxValues, 2):
    # Analog The ONE
    bagOfMax_AV[i] = -999999.99
    bagOfMin_AV[i] = +999999.99
    



filePath = "/tmp/theBatt.txt"

def writeStringToFile(s):
    global filePath
    
    with open(filePath, "a") as f:
        f.write(s)
    
    
    
nuvarande_klockslag = datetime.now().strftime("%H:%M:%S")
totalFileText = ""



def createBattPage(battSample: BattSample):
        
    batteryData = {
        "pageUpdatedTime"  : datetime.now().strftime("%H:%M:%S"),
        "socStateOfCharge" : battSample.socStateOfCharge,
        "cycleCounter"     : battSample.cycleCounter,
        "roundedTemp"     : battSample.roundedTemp,        
        "capacityAh"       : battSample.capacityAh,
        "totalCapacityAh"  : battSample.totalCapacityAh,
        "v1"               : round(battSample.v1, 3),
        "v2"               : round(battSample.v2, 3),
        "v3"               : round(battSample.v3, 3),
        "v4"               : round(battSample.v4, 3),
        "v1PixelHeight"    : round((battSample.v1-3.2)*500, 0),
        "v2PixelHeight"    : round((battSample.v2-3.2)*500, 0),
        "v3PixelHeight"    : round((battSample.v3-3.2)*500, 0),
        "v4PixelHeight"    : round((battSample.v4-3.2)*500, 0),
        "vDiffmV"          : battSample.vDiffmV,
        "vTotal"           : round(battSample.v1 + battSample.v2 + battSample.v3 + battSample.v4, 2)
    }
    # 1. Läs in din HTML-mall
    with open("BattTemplate_DoubleBirdwings.html", "r", encoding="utf-8") as f:
        html_mall_innehall = f.read()

    # 2. Skapa en Jinja2-mall och baka in värdena
    mall = Template(html_mall_innehall)
    print(f"\nbatteryData = {batteryData}\n\n")
    fardig_html = mall.render(batteryData)

    # 3. Spara den färdiga HTML-sidan (som du sedan kan öppna i webbläsaren)
    with open("/tmp/BattPage.html", "w", encoding="utf-8") as f:
        f.write(fardig_html)

    print("HTML-sidan har uppdaterats!")


    
    
    
    
    
    
    
    
    
    
    
def validate_and_parse(frame):
    global pos_cycleCounter
    global pos_SOC
    global pos_temperature
    global NrOfValues
    global minTemp
    global maxTemp
    global minSOC
    global maxSOC
    global minDiff_mV
    global maxDiff_mV
    global thrownResults
    global sekunder_sedan_start
    global nuvarande_klockslag
    global totalFileText
    global start_tid

    sekunder_sedan_start = time.monotonic() - start_tid
    nuvarande_datum      = datetime.now()
    datum_klockslag  = nuvarande_datum.strftime(f"%Y-%m-%d %H:%M:%S    Sekunder sedan start: {sekunder_sedan_start}      thrown={thrownResults}")

    lFrame = frame.upper().strip()
    #lFrame = frame.upper()

    dPrint(f"validate_and_parse(), requestBuffer = {requestBuffer}")
    
    pos_StartPattern = lFrame.find(StartPattern)    
    dPrint(f"validate_and_parse(), pos_StartPattern = {pos_StartPattern}")    

    # DB80 when cycle=53, Now with 54 it doesn't find DB80......54=36
    if pos_StartPattern != -1:
        dPrint(f"validate_and_parse(), FOUND {StartPattern}!!!!!!     pos_StartPattern = {pos_StartPattern}")
    else:
        dPrint(f"validate_and_parse(), didn't find StartPattern ({StartPattern})\n{lFrame}")
        return

    #########################################################################3
    #########################################################################3
    #########################################################################3
    pos_StartPattern = pos_StartPattern + pos_Offset
    #########################################################################3
    #########################################################################3
    #########################################################################3

    startFrame = lFrame[pos_StartPattern:]
    origFrame = frame
    frame = ""
    #dPrint(f"pos_cycleCounter = {pos_cycleCounter}")
    #dPrint(f"pos_SOC          = {pos_SOC}")
    #dPrint(f"pos_temperature  = {pos_temperature}")
    #dPrint(f"pos_v1  = {pos_v1}")
    #dPrint(f"pos_v2  = {pos_v2}")
    #dPrint(f"pos_v3  = {pos_v3}")
    #dPrint(f"pos_v4  = {pos_v4}")

    cycleCounter = "Unset"
    SocStateOfCharge = "Unset"
    temp = "Unset"
    v1 =  "Unset"
    v2 =  "Unset"
    v3 =  "Unset"
    v4 =  "Unset"

    for i in range(pos_cycleCounter-4, NrOfMinMaxValues, 4):
        b1 = startFrame[i:i+2]
        b2 = startFrame[i+2:i+4]
        hexVal         = f"{b1}{b2}"
        hexWrappedVal  = f"{b2}{b1}"

        dPrint(f"hexVal={hexVal}       hexWrappedVal={hexWrappedVal}")
        
        dv  = hex_to_uint16(hexVal)
        dPrint(f"dv = {dv}")

        dvSigned = hex_to_int16(hexVal)
        dPrint(f"dvSigned = {dvSigned}")

        dvWrapped = hex_to_uint16(hexWrappedVal)
        dPrint(f"dvWrapped = {dvWrapped}")

        dvWrappedSigned = hex_to_int16(hexWrappedVal)        
        dPrint(f"dvWrappedSigned = {dvWrappedSigned}")
        
        # Analog the ONE
        avTheOne = calcAnalog16bitFromSignedHex(hexWrappedVal)

        if i == pos_cycleCounter:
            cycleCounter = dvWrapped
        elif i == pos_SOC:
            SocStateOfCharge = dvWrapped
        elif i == pos_temperature:
            dPrint(f"temp calculation, hexVal={hexVal}, hexWrappedVal={hexWrappedVal}, dv={dv}, dvWrapped={dvWrapped}, dvSigned={dvSigned}, dvSigned={dvWrappedSigned}")
            temp, _ = calcTemp(dvWrapped)
        elif i == pos_v1:
            v1 = avTheOne
            dPrint(f"v1 = {v1}")
        elif i == pos_v2:
            v2 = avTheOne
            dPrint(f"v2 = {v2}")
        elif i == pos_v3:
            v3 = avTheOne
            dPrint(f"v3 = {v3}")
        elif i == pos_v4:
            v4 = avTheOne
            dPrint(f"v4 = {v4}")
        else:
            s = ".-."
        
        # Analog The ONE
        bagOfMin_AV[i] = min(bagOfMin_AV[i], avTheOne)
        bagOfMax_AV[i] = max(bagOfMax_AV[i], avTheOne)
                   
        decVal        = hex_to_uint16(hexVal)
        decWrappedVal = hex_to_uint16(hexWrappedVal)                
    
    total_V, diff_mV         = calcMinMax(v1, v2, v3, v4)
    fullCapacity             = 98.5
    currCapacity             = fullCapacity*SocStateOfCharge/100
    
    if (v1 < throwLowLimit) or (v2 < throwLowLimit) or (v3 < throwLowLimit) or (v4 < throwLowLimit):
        thrownResults += 1
        print(f"ThrownnResults = {thrownResults}")
        print(f"Throw temp result.....v1={v1}, v1={v2}, v1={v3}, v1={v4},    throwLowLimit = {throwLowLimit}")
        print(f"Thrown frame = {origFrame}\n\n\n")
        return False
        
    else:
        minTemp = min(minTemp, temp)
        maxTemp = max(maxTemp, temp)
        minSOC = min(minSOC, SocStateOfCharge)
        maxSOC = max(maxSOC, SocStateOfCharge)
        
        minDiff_mV = min(minDiff_mV, diff_mV)
        maxDiff_mV = max(maxDiff_mV, diff_mV)

    roundedTemp = round(temp, 1)
    roundedCapacity = round(fullCapacity * SocStateOfCharge/100,1)
    battSample = BattSample(
        dayTime           = datum_klockslag,
        secondsRun        = 123,
        cycleCounter      = cycleCounter,
        socStateOfCharge  = SocStateOfCharge,
        capacityAh        = f"{roundedCapacity}",
        totalCapacityAh   = "98,5",
        roundedTemp       = roundedTemp,
        v1                = v1,
        v2                = v2,
        v3                = v3,
        v4                = v4,
        minDiffmV         = minDiff_mV,
        maxDiffmV         = maxDiff_mV,
        vDiffmV           = diff_mV,
        thrownResults     = thrownResults
    )

    createBattPage(battSample)
    
    sampleText = f"\n\nLEGACYYYYYYYYYYYYYYYYY\n"    
    sampleText += f"\n\n{datum_klockslag}" + "\n"
    sampleText += f"--------- Cycle Counter     : {cycleCounter}" + "\n"
    sampleText += f"--------- SOC               : {SocStateOfCharge}          ({minSOC} .. {maxSOC})" + "\n"
    sampleText += f"--------- fullCapacity      : {fullCapacity}" + "\n"
    sampleText += f"--------- currCapacity      : {currCapacity}" + "\n"
    #print(f"--------- Exact Temp       : {temp} grader ({minTemp} .. {maxTemp})"
    sampleText += f"--------- Temp              : {roundedTemp} grader" + "\n"
    sampleText += f"--------- v1                : {v1} V" + "\n"
    sampleText += f"--------- v2                : {v2} V" + "\n"
    sampleText += f"--------- v3                : {v3} V" + "\n"
    sampleText += f"--------- v4                : {v4} V" + "\n"
    sampleText += f"--------- vTotal            : {total_V} V" + "\n"
    sampleText += f"--------- Diff:             : {diff_mV} mV ({minDiff_mV} .. {maxDiff_mV})mV" + "\n"
    sampleText += f"--------- Thrown results    : {thrownResults} times" + "\n" + "\n"

    hotText = f"\n\nHOTHOTHOTTTTTTTTTTTTTtt!\n"    
    hotText += f"Date: {battSample.dayTime}" + "\n"
    hotText += f"--------- Cycle Counter     : {battSample.cycleCounter}" + "\n"
    hotText += f"--------- SOC               : {battSample.socStateOfCharge}          ({minSOC} .. {maxSOC})" + "\n"
    hotText += f"--------- fullCapacity      : {fullCapacity}" + "\n"
    hotText += f"--------- currCapacity      : {fullCapacity * battSample.socStateOfCharge/100}" + "\n"
    #print(f"--------- Exact Temp       : {temp} grader ({minTemp} .. {maxTemp})"
    hotText += f"--------- Temp              : {battSample.roundedTemp} grader" + "\n"
    hotText += f"--------- v1                : {battSample.v1} V" + "\n"
    hotText += f"--------- v2                : {battSample.v2} V" + "\n"
    hotText += f"--------- v3                : {battSample.v3} V" + "\n"
    hotText += f"--------- v4                : {battSample.v4} V" + "\n"
    hotText += f"--------- minDiffmV         : {battSample.minDiffmV} mV" + "\n"
    hotText += f"--------- maxDiffmV         : {battSample.maxDiffmV} mV" + "\n"
    calcedTotalV = battSample.v1 + battSample.v2 + battSample.v3 + battSample.v4
    hotText += f"--------- vTotal            : {calcedTotalV} V\n" + "\n"
    hotText += f"--------- Diff:             : {battSample.vDiffmV} mV ({minDiff_mV} .. {maxDiff_mV})mV" + "\n"
    hotText += f"--------- Thrown results    : {battSample.thrownResults} times" + "\n" + "\n"





    print(f"{sampleText}")
    
    battPage = createBattPage(battSample)

    print(f"Batt page = {battPage}")
    
    totalFileText += sampleText
    writeStringToFile(totalFileText)


    return True
    
    # Sök efter SOC-markör (63) och Cykel-markör (35) från position 10
    start_search = 10
    debugPrint(dbg, f"pos_StartPattern={pos_StartPattern}   Pettra was here!")
    frameDB80 = lFrame[pos_StartPattern:]
    print(f"pos_StartPattern={pos_StartPattern}   Pettra was here!")





    pos_cycle_marker = 6
    pos_soc_marker = 10

    print(f"Cycle counter = {hex_to_uint16(frameDB80[pos_cycle_marker:])}")
    print(f"SOC           = {hex_to_uint16(frameDB80[pos_soc_marker:])}")

    # Validera att de finns på jämna positioner
    #is_valid_soc = pos_soc_marker != -1 and pos_soc_marker % 2 == 0
    #is_valid_cyc = pos_cycle_marker != -1 and pos_cycle_marker % 2 == 0



    print(f"\n--- NY Mätning ---")
    print(f"M[22-23]    ={frameDB80[22]}{frameDB80[23]}")
    print(f"M[26-27]    ={frameDB80[26]}{frameDB80[27]}")
    print(f"M[44-47]    ={frameDB80[44]}{frameDB80[45]}{frameDB80[46]}{frameDB80[47]}")
    print(f"M[48-51]    ={frameDB80[48]}{frameDB80[49]}{frameDB80[50]}{frameDB80[51]}")
    print(f"M[52-55]    ={frameDB80[52]}{frameDB80[53]}{frameDB80[54]}{frameDB80[55]}")
    print(f"M[56-59]    ={frameDB80[56]}{frameDB80[57]}{frameDB80[58]}{frameDB80[59]}")
    
    print(f"Markör-positioner:")
    print(f"   - SOC-markör ('63') hittad på index: {pos_soc_marker}")
    print(f"   - Cykel-markör ('35') hittad på index: {pos_cycle_marker}")        
    print(f"Temperaturen är: {round(celsius, 1)} °C")

    print(f"Ström-kandidater (Hex-värden):")
    # Vi kollar tre vanliga positioner för ström i detta protokoll
    c1 = frameDB80[pos_soc_marker-8:pos_soc_marker-4]
    val1 = int(c1, 16) / 1000
    c2 = frameDB80[pos_soc_marker-4:pos_soc_marker]
    val2 = int(c2, 16) / 1000        
    c3 = frameDB80[pos_soc_marker+4:pos_soc_marker+8] # Ofta SOC % här, men kan vara ström
    val3 = int(c3, 16) / 1000

    print(f"c1[pos_soc_marker -8..-4]={c1}, val1={val1}")
    print(f"c2[pos_soc_marker -4..-0]={c2}, val2={val2}")
    print(f"c3[pos_soc_marker +4..+8]={c3}, val3={val3}")

#        print(f"   Pos A (idx {pos_soc_marker-8}): {c1} -> {hex_to_signed_int(c1)/100 if len(c1)==4 else '?'} A")
#        print(f"   Pos B (idx {pos_soc_marker-4}): {c2} -> {hex_to_signed_int(c2)/100 if len(c2)==4 else '?'} A")
#        print(f"   Pos C (idx {pos_soc_marker+4}): {c3} -> {hex_to_signed_int(c3)/100 if len(c3)==4 else '?'} A")
        
    exit
    
    try:
        # Identifiera celler och deras positioner
        cells = []
        foundgood_i = - 1
        for i in range(0, len(frameDB80)-3, 2):
            chunk = frameDB80[i:i+4]
            if chunk.startswith("0D"):
                val = int(chunk, 16) / 1000
                if 3.0 < val < 3.8:
                    cells.append((i, val))
                    foundgood_i = i

        if cells:
            print(f"🔋 Cellstatus:")
            total_v = 0
            for idx, (pos, v) in enumerate(cells[:4], 1):
                print(f"   Cell {idx}: {v:.3f}V (index {pos})")
                total_v += v
            print(f"   Totalspänning: {total_v:.2f}V")
            print(f"   FoundGood_i  : #{foundgood_i}")
        
        # Tips: SOC-värdet i % brukar finnas 2-4 steg efter markören "63"
        # Vi kan titta på vad som finns där:
        potential_soc_hex = frameDB80[pos_soc_marker+2:pos_soc_marker+6]
        print(f"📊 Potentiellt SOC-värde (hex efter markör): {potential_soc_hex}")

    except Exception as e:
        print(f"⚠️ Fel vid tolkning: {e}")
    




def dPrint(str):
    global dbgPrinting
    
    if dbgPrinting == True:
        print(str)




        




def callback(sender, data):
    global buffer
    global requestBuffer
    global newValueWasFound
    global dbgPrinting
    global callbackNr
    
    print(f"callback(), START!!!!!!!!!!!")
    if requestBuffer == False:
        print(f"callback(), requestBuffer == False......return #{callbackNr} START")
        return
        
    callbackNr += 1

    print(f"callback() #{callbackNr} START")

    # \r gör att raden skrivs över istället för att skapa nya rader
    #### print(f"callback() #{callbackNr} START, Klockan: {nuvarande_klockslag} | Sekunder sedan start: {sekunder_sedan_start:.2f} s", end="\r")
                
    dPrint(f"callback()!!!\nsender={sender}\ndata={data}     When debugging!")
                
    chunk = data.decode('ascii', errors='ignore')
    buffer += chunk
    print(f"size of buffer = {len(buffer)}\nbuffer={buffer}\n\n")
    
    # Vi väntar tills vi har ett rejält block innan vi analyserar
    #print(f"Buffer len = {len(buffer)}")                
    
    newValueWasFound = False
    if len(buffer) > 230:
        requestBuffer = False                        
        try:
            sendBuffer = buffer
            buffer = ""
            print(f"\n\n>>>>>>>>TTTTTTTT230, Call validate_and_parse......BEGIN, len(buffer)={len(sendBuffer)}")                    
            dPrint(f"\n{sendBuffer}")                    
                        
            # NOW is the moment....is it a valid Buffer and parsed OK?
            newValueWasFound = validate_and_parse(sendBuffer)
            print(f"TTTTTTTTcallback(), Call validate_and_parse")
        finally:            
            print(f"FFFFFFFFFFcallback(), Finally......END")            

    dPrint(f"callback(), Before last if requestBuffer, requestBuffer={requestBuffer}")
    
    #if newValueWasFound and is_parsing:
    #    print(f"callback() Value OK, Sleep!!! Before sleep")
    #    time.sleep(SleepTimeBetweenMeasurements)
    #    print(f"callback() Value OK, Sleep!!! After sleep")
    #else:
    #    dPrint(f"callback() Value NOK when Parsing, don't sleep!!!     callbackNr = {callbackNr}")

    #is_parsing = False
    #print(f"callback() #{callbackNr} ENDENDENDENDEND, Do NOT sleep 10")
    ##time.sleep(10)
    #print(f"callback() #{callbackNr} ENDENDENDENDEND, ENDDDDDDDDDDDDDDDDDD")
    return

async def run_monitor():
    global requestBuffer
    global newValueWasFound    
    global SleepTimeBetweenMeasurements
    
    print(f"Ansluter till SkanBatt...")
    client = BleakClient(ADDRESS)

    while True:
    
        try:
            print(f"await client.connect()...")
            await client.connect()
            print(f"...client.connect(), READY!")
            buffer = ""
        except Exception as e:
            print(f"client.connect() Failed: {e}")


        try:
            print(f"await client.start_notify(NOTIFY_UUID, callback)...")
            await client.start_notify(NOTIFY_UUID, callback)
            print(f"...client.start_notify(NOTIFY_UUID, callback), READY!    Lyssnar... (Bryt med Ctrl+C)")
                    
            requestBuffer = True        
            while newValueWasFound != True:
                print(f"---------------await asyncio.sleep(5)......")
                print(f"---------------run_monitor(), requestBuffer = {requestBuffer}")
            
                await asyncio.sleep(1)
                # time.sleep(SleepTimeBetweenMeasurements)

                print(f"---------------...asyncio.sleep(10) READY!")
                                
        except Exception as e:
            print(f"Anslutningsfel: {e}")
        finally:
            print(f"---------------...STOP Nofity!")
            print(f"---------------...STOP Nofity!")
            print(f"---------------...STOP Nofity!")
            await client.stop_notify(NOTIFY_UUID)                
            
            
        print(f"await client.disconnect()...")
        print(f"await client.disconnect()...")
        print(f"await client.disconnect()...")
        print(f"await client.disconnect()...")
        print(f"await client.disconnect()...")
        print(f"await client.disconnect()...")
        await client.disconnect()
        print(f"...client.disconnect(), READY!")
        print(f"...client.disconnect(), READY!")
        print(f"...client.disconnect(), READY!")
        print(f"...client.disconnect(), READY!")
        print(f"---------Sleep 60")
        print(f"---------Sleep 60")
        print(f"---------Sleep 60")
        print(f"---------Sleep 60")
        print(f"---------Sleep 60")
        print(f"---------Sleep 60")
        print(f"---------Sleep 60")
        time.sleep(60)

if __name__ == "__main__":
    print(f"---------START MAIN run_monitor-----------")
    print(f"---------START MAIN run_monitor-----------")
    print(f"---------START MAIN run_monitor-----------")
    print(f"---------START MAIN run_monitor-----------")
    print(f"---------START MAIN run_monitor-----------")
    
    try:
        asyncio.run(run_monitor())
    except Exception as e:
        print(f"Exception::::::::::::run_monitor: {e}")
        print(f"Exception::::::::::::run_monitor: {e}")
        print(f"Exception::::::::::::run_monitor: {e}")
        print(f"Exception::::::::::::run_monitor: {e}")
        print(f"Exception::::::::::::run_monitor: {e}")
        
            
        
    print(f"---------END MAIN run_monitor-----------")
    print(f"---------END MAIN run_monitor-----------")
    print(f"---------END MAIN run_monitor-----------")
    print(f"---------END MAIN run_monitor-----------")
    print(f"---------END MAIN run_monitor-----------")













































# Tips för din HTML-dashboard

# Eftersom du bygger en dashboard för detta, kan det vara smart att programmera in en färgindikator för "Differensen":
# 
#     GRÖN (0 - 50 mV): Allt är perfekt.
# 
#     GUL (51 - 100 mV): Ok, men systemet jobbar med balansering.
# 
#     RÖD (> 100 mV): Varning, obalans eller en cell som börjar bli dålig/full mycket snabbare än de andra.




################




