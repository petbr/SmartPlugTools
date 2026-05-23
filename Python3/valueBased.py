import time
from datetime import datetime
import asyncio
from PettraHelpers import *

from bleak import BleakClient


# Spara starttiden direkt när programmet startar
start_tid = time.monotonic()

print(f"Programmet startade: {datetime.now().strftime('%H:%M:%S')}")

ADDRESS = "B0:B1:13:75:11:12"
NOTIFY_UUID = "0000ffe4-0000-1000-8000-00805f9b34fb"
SleepTimeBetweenMeasurements = 20

DEBUG = True  # Ändra till False när du är nöjd
is_parsing = False    # Global flagga
buffer = ""

########################
pos_Offset       = 0
########################

StartPattern     = "800100"

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
bagOfMax_Analog_Values = [0]*NrOfMinMaxValues
bagOfMin_Analog_Values = [0]*NrOfMinMaxValues

# Analog The ONE
bagOfMax_AV = [0]*NrOfMinMaxValues
bagOfMin_AV = [0]*NrOfMinMaxValues

# Normal
bagOfMax_Digital_Values       = [0]*NrOfMinMaxValues
bagOfMin_Digital_Values       = [0]*NrOfMinMaxValues
bagOfMax_DigitalSigned_Values = [0]*NrOfMinMaxValues
bagOfMin_DigitalSigned_Values = [0]*NrOfMinMaxValues


# Wrapped
bagOfMax_WrappedDigital_Values       = [0]*NrOfMinMaxValues
bagOfMin_WrappedDigital_Values       = [0]*NrOfMinMaxValues
bagOfMax_WrappedDigitalSigned_Values = [0]*NrOfMinMaxValues
bagOfMin_WrappedDigitalSigned_Values = [0]*NrOfMinMaxValues

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
    
# Analog legacy
    bagOfMax_Analog_Values[i] = -999999.99
    bagOfMin_Analog_Values[i] = +999999.99

    # Normal
    bagOfMin_Digital_Values[i]              = 65535
    bagOfMax_Digital_Values[i]              = 0
    bagOfMin_DigitalSigned_Values[i]        = 32767
    bagOfMax_DigitalSigned_Values[i]        = -32768
    # Wrapped
    bagOfMin_WrappedDigital_Values[i]       = 65535
    bagOfMax_WrappedDigital_Values[i]       = 0
    bagOfMin_WrappedDigitalSigned_Values[i] = 32767
    bagOfMax_WrappedDigitalSigned_Values[i] = -32768



def extraText(i, h):
    global pos_cycleCounter
    global pos_SOC
    global pos_temperature

#    if i == pos_temperature:
#        return f"  Temperature...don't calculate here"

    analogueValue  = calcAnalog16bit(h)
    digital16Value = calcDigital16bit(h)
    
    extraDigitalText = f"{digital16Value}, min={bagOfMin_Digital_Values[i]}, max={bagOfMax_Digital_Values[i]}"
    extraAnalogText = f"{analogueValue}, min={bagOfMin_Analog_Values[i]}, max={bagOfMax_Analog_Values[i]}"
    
    extraAnalogDigitalText = f"{extraDigitalText}, {extraAnalogText}"
    
    if i == pos_cycleCounter:
        extraText = f"  CycleCounter={extraAnalogDigitalText}"
    elif i == pos_SOC:
        extraText = f"  SOC={extraAnalogDigitalText}"
    elif i == pos_v1:
        v1 = analogueValue
        extraText = f"  v1={v1}V, {extraAnalogDigitalText}"
    elif i == pos_v2:
        v2 = analogueValue
        extraText = f"  v2={v2}V, {extraAnalogDigitalText}"
    elif i == pos_v3:
        v3 = analogueValue
        extraText = f"  v3={v3}V, {extraAnalogDigitalText}"
    elif i == pos_v4:        
        v4 = analogueValue
        extraText = f"  v4={v4}V, {extraAnalogDigitalText}"
    else:
        try:
            extraText = f"        current = , {extraAnalogDigitalText}" 
        except ValueError:
            c = 0
            extraText = "----bad characters----"
        
    return extraText



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
    
    lFrame = frame.upper().strip()
    #lFrame = frame.upper()

    dPrint(f"validate_and_parse(), is_parsing = {is_parsing}")
    
    #########################################################################3
    print(f"validate_and_parse(), db80Frame =")
    print(f"                                                                                                    1         1         1         1         1")
    print(f"0         1         2         3         4         5         6         7         8         9         0         1         2         3         4")
    print(f"012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890")
    print(f"{lFrame}")

    pos_StartPattern = lFrame.find(StartPattern)
    
    print(f"validate_and_parse(), pos_StartPattern = {pos_StartPattern}")    
    #########################################################################3

    # DB80 when cycle=53, Now with 54 it doesn't find DB80......54=36
    if pos_StartPattern != -1:
        print(f"validate_and_parse(), FOUND {StartPattern}!!!!!!     pos_StartPattern = {pos_StartPattern}")
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

    db80Frame = lFrame[pos_StartPattern:]
    frame = ""
    dPrint(f"pos_cycleCounter = {pos_cycleCounter}")
    dPrint(f"pos_SOC          = {pos_SOC}")
    dPrint(f"pos_temperature  = {pos_temperature}")
    dPrint(f"pos_v1  = {pos_v1}")
    dPrint(f"pos_v2  = {pos_v2}")
    dPrint(f"pos_v3  = {pos_v3}")
    dPrint(f"pos_v4  = {pos_v4}")

    cycleCounter = "Unset"
    SocStateOfCharge = "Unset"
    temp = "Unset"
    v1 =  "Unset"
    v2 =  "Unset"
    v3 =  "Unset"
    v4 =  "Unset"

    for i in range(pos_cycleCounter-4, NrOfMinMaxValues, 4):
        b1 = db80Frame[i:i+2]
        b2 = db80Frame[i+2:i+4]
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
            print(f"temp calculation, hexVal={hexVal}, hexWrappedVal={hexWrappedVal}, dv={dv}, dvWrapped={dvWrapped}, dvSigned={dvSigned}, dvSigned={dvWrappedSigned}")
            temp, _ = calcTemp(dvWrapped)
        elif i == pos_v1:
            v1 = avTheOne
            print(f"v1 = {v1}")
        elif i == pos_v2:
            v2 = avTheOne
            print(f"v2 = {v2}")
        elif i == pos_v3:
            v3 = avTheOne
            print(f"v3 = {v3}")
        elif i == pos_v4:
            v4 = avTheOne
            print(f"v4 = {v4}")
        else:
            s = ".-."
        
  
 
        # bagOfMin_WrappedDigitalSigned_Values

        # Normal
        bagOfMin_Digital_Values[i]  = min(bagOfMin_Digital_Values[i], dv)
        bagOfMax_Digital_Values[i]  = max(bagOfMax_Digital_Values[i], dv)
        bagOfMin_DigitalSigned_Values[i] = min(bagOfMin_DigitalSigned_Values[i], dvSigned)
        bagOfMax_DigitalSigned_Values[i] = max(bagOfMax_DigitalSigned_Values[i], dvSigned)
        
        curMin = bagOfMin_Digital_Values[i]
        curMax = bagOfMax_Digital_Values[i]
        curSignedMin = bagOfMin_DigitalSigned_Values[i]
        curSignedMax = bagOfMax_DigitalSigned_Values[i]

        # Wrapped
        bagOfMin_WrappedDigital_Values[i]  = min(bagOfMin_WrappedDigital_Values[i], dvWrapped)
        bagOfMax_WrappedDigital_Values[i]  = max(bagOfMax_WrappedDigital_Values[i], dvWrapped)
        bagOfMin_WrappedDigitalSigned_Values[i] = min(bagOfMin_WrappedDigitalSigned_Values[i], dvWrappedSigned)
        bagOfMax_WrappedDigitalSigned_Values[i] = max(bagOfMax_WrappedDigitalSigned_Values[i], dvWrappedSigned)
        
        curWrappedMin = bagOfMin_WrappedDigital_Values[i]
        curWrappedMax = bagOfMax_WrappedDigital_Values[i]
        curWrappedSignedMin = bagOfMin_WrappedDigitalSigned_Values[i]
        curWrappedSignedMax = bagOfMax_WrappedDigitalSigned_Values[i]
        
        normalStr        = f"hex=${hexVal} = {dv:5d} ({curMin: 6d}..{curMax: 6d}) "
        normalSignedStr  = f"hex=${hexVal} = {dvSigned:5d} ({curSignedMin: 6d}..{curSignedMax: 6d}) "
        
        wrappedStr       = f"hex=${hexWrappedVal} = {dvWrapped:5d} ({curWrappedMin: 6d}..{curWrappedMax: 6d}) "
        wrappedSignedStr = f"hex=${hexWrappedVal} =  {dvWrappedSigned:5d} ({curWrappedSignedMin: 6d}..{curWrappedSignedMax: 6d}) "

        
        analogueValue  = calcAnalog16bit(hexVal)
        digital16Value = calcDigital16bit(hexVal)

        
        # Analog The ONE
        bagOfMin_AV[i] = min(bagOfMin_AV[i], avTheOne)
        bagOfMax_AV[i] = max(bagOfMax_AV[i], avTheOne)
            
        # Analog legacy
        bagOfMin_Analog_Values[i] = min(bagOfMin_Analog_Values[i], analogueValue)
        bagOfMax_Analog_Values[i] = max(bagOfMax_Analog_Values[i], analogueValue)

        # bagOfMin_WrappedDigitalSigned_Values    
        bagOfMin_Digital_Values[i] = min(bagOfMin_Digital_Values[i], digital16Value)
        bagOfMax_Digital_Values[i] = max(bagOfMax_Digital_Values[i], digital16Value)

        
        
        decVal        = hex_to_uint16(hexVal)
        decWrappedVal = hex_to_uint16(hexWrappedVal)
        
        if i == pos_temperature:
            tempText = "tempAtPos"
        else:
            tempText = "temp"
            
        #hexWrapVal  = db80Frame[i+2:i+4] + db80Frame[i:i+2]
        #decWrapVal  = hex_to_uint16(hexWrapVal)
        et     = extraText(i, hexVal)   #Until we know better
        etWrap = extraText(i, hexWrappedVal)   #Until we know better

        print(f"-----------------------------------------------------------")
        print(f"i = {i:3}             {posToKnownFeature(i)}")
        print(f"AV = {calcAnalog16bitFromSignedHex(hexWrappedVal)}")
        calcAnalog16bitFromSignedHex(hexWrappedVal)
        print(f"N: {normalStr}   NS:{normalSignedStr}")
        print(f"W: {wrappedStr}   WS:{wrappedSignedStr}")

        _, _, temp_at_i        = calc_Uint16_HexStr_Temp(hexVal)
        _, _, temp_atWrapped_i = calc_Uint16_HexStr_Temp(hexWrappedVal)

        # print(f"i = {i:3},     dv  = {dv}\n             ${hexWrappedVal} ({bagWrappedMin: 6d}...{bagWrappedMax: 6d})    dvS = {dvS}       __{db80Frame[i:i+10]}\n")


        print(f"TheONE i = {i},   avTheOne={avTheOne},                                           {bagOfMin_AV[i]} .. {bagOfMax_AV[i]}")
        #print(f"EEEEEEEE i = {i:03}, ${hexWrappedVal} = {decWrappedVal:05}{etWrap}, {tempText}={temp_atWrapped_i}     WRAPPED\n")
        print(f"-----------------------------------------------------------")
    
    print(f"\n")
    print(f"NewlyCalculated: cycleCounter={cycleCounter}, SocStateOfCharge={SocStateOfCharge}, temp={temp}, v1={v1}, v1={v2}, v1={v3}, v1={v4}")

    cycle_CounterStr = db80Frame[pos_cycleCounter:pos_cycleCounter+4]
    SOC_Str          = db80Frame[pos_SOC:pos_SOC+4]
    temp_Str         = db80Frame[pos_temperature:pos_temperature+4]
    v1_Str           = db80Frame[pos_v1:pos_v1+4]
    v2_Str           = db80Frame[pos_v2:pos_v2+4]
    v3_Str           = db80Frame[pos_v3:pos_v3+4]
    v4_Str           = db80Frame[pos_v4:pos_v4+4]
    


    
    dPrint(f"cycleCounter     = {cycleCounter}")
    dPrint(f"SocStateOfCharge = {SocStateOfCharge}")
    dPrint(f"temp_Str         = {temp_Str}")
    dPrint(f"v1_Str           = {v1_Str}")
    dPrint(f"v2_Str           = {v2_Str}")
    dPrint(f"v3_Str           = {v3_Str}")
    dPrint(f"v4_Str           = {v4_Str}")

    dPrint(f"cycle")
    ui16_Cycle_Counter       = hex_to_uint16(cycle_CounterStr)
    dPrint(f"SOC")
    ui16_SOC_Counter         = hex_to_uint16(SOC_Str)
    dPrint(f"Temp")
    _, _, temp               = calc_Uint16_HexStr_Temp(temp_Str)
    temp                     = round(temp,1)
    #v1                       = calcAnalog16bit(v1_Str)
    #v2                       = calcAnalog16bit(v2_Str)
    #v3                       = calcAnalog16bit(v3_Str)
    #v4                       = calcAnalog16bit(v4_Str)
    total_V, diff_mV         = calcMinMax(v1, v2, v3, v4)
    fullCapacity             = 98.5
    currCapacity             = fullCapacity*SocStateOfCharge/100
    
    if (v1 == 0.0) or (v2 == 0.0) or (v3 == 0.0) or (v4 == 0.0):
        print(f"Throw temp result.....v1={v1}, v1={v2}, v1={v3}, v1={v4}, ")
    else:
        minTemp = min(minTemp, temp)
        maxTemp = max(maxTemp, temp)
        minSOC = min(minSOC, SocStateOfCharge)
        maxSOC = max(maxSOC, SocStateOfCharge)
        
        minDiff_mV = min(minDiff_mV, diff_mV)
        maxDiff_mV = max(maxDiff_mV, diff_mV)

    
    print(f"--------- ui16_Cycle_Counter: {cycleCounter}")
    print(f"--------- SOC               : {SocStateOfCharge}          ({minSOC} .. {maxSOC})")
    print(f"--------- fullCapacity      : {fullCapacity}")
    print(f"--------- currCapacity      : {currCapacity}")
    print(f"--------- Temperature       : {temp} grader ({minTemp} .. {maxTemp})")
    print(f"--------- v1                : {v1} V")
    print(f"--------- v2                : {v2} V")
    print(f"--------- v3                : {v3} V")
    print(f"--------- v4                : {v4} V")
    print(f"--------- vTotal            : {total_V} V")
    print(f"--------- Diff:             : {diff_mV} mV ({minDiff_mV} .. {maxDiff_mV})mV")
    
    

    return
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
    global is_parsing
    global dbgPrinting
    
    sekunder_sedan_start = time.monotonic() - start_tid
    nuvarande_klockslag = datetime.now().strftime("%H:%M:%S")
        
    # \r gör att raden skrivs över istället för att skapa nya rader
    print(f"Klockan: {nuvarande_klockslag} | Sekunder sedan start: {sekunder_sedan_start:.2f} s", end="\r")
    #print(f"Klockan: {nuvarande_klockslag} | Sekunder sedan start: {sekunder_sedan_start:.2f} s")
            
    dPrint(f"callback()!!!\nsender={sender}\ndata={data}     When debugging!")
                
    chunk = data.decode('ascii', errors='ignore')
    buffer += chunk
    dPrint(f"size of buffer = {len(buffer)}\nbuffer={buffer}\n\n")
    
    # Vi väntar tills vi har ett rejält block innan vi analyserar
    #print(f"Buffer len = {len(buffer)}")                
    if len(buffer) > 230:
        is_parsing = True                        
        try:
            sendBuffer = buffer
            buffer = ""
            dPrint(f"\n\n>230, Call validate_and_parse......BEGIN, len(buffer)={len(sendBuffer)}")                    
            validate_and_parse(sendBuffer)
            dPrint(f"Call validate_and_parse......END")
        finally:
            is_parsing = False  # Now finished and can retrieve next chunk

    dPrint(f"End of callback() ENDENDENDENDENDENDENDENDENDENDENDENDENDEND")

async def run_monitor():
    print(f"Ansluter till SkanBatt...")
    client = BleakClient(ADDRESS)
    
    try:
        print(f"await client.connect()...")
        await client.connect()
        print(f"...client.connect(), READY!")
        buffer = ""


        print(f"await client.start_notify(NOTIFY_UUID, callback)...")
        await client.start_notify(NOTIFY_UUID, callback)
        print(f"...client.start_notify(NOTIFY_UUID, callback), READY!    Lyssnar... (Bryt med Ctrl+C)")
                
        while True:
            dPrint(f"await asyncio.sleep(10)......")
            await asyncio.sleep(1)
            time.sleep(SleepTimeBetweenMeasurements)

            dPrint(f"...asyncio.sleep(10) READY!")
            
    except Exception as e:
        print(f"Anslutningsfel: {e}")
    finally:
        print(f"await client.disconnect()...")
        await client.disconnect()
        print(f"...client.disconnect(), READY!")

if __name__ == "__main__":
    asyncio.run(run_monitor())














































async def run_monitor_Orig():
    print(f"Ansluter till SkanBatt...")
    client = BleakClient(ADDRESS)
    
    try:
        await client.connect()
        buffer = ""

        def callback(sender, data):
            nonlocal buffer
            print(f"callback!!!!!!!!")
            try:
                chunk = data.decode('ascii', errors='ignore')
                buffer += chunk
                
                # Vi väntar tills vi har ett rejält block innan vi analyserar
                print(f"Buffer len = {len(buffer)}")
                if len(buffer) > 360:
                    print(f"Call validate_and_parse......BEGIN, length={len(buffer)}")
                    validate_and_parse(buffer)
                    print(f"Call validate_and_parse......END")
                    buffer = "" 
            except: pass

        await client.start_notify(NOTIFY_UUID, callback)
        print("Lyssnar... (Bryt med Ctrl+C)")
        
        while True:
            print(f"await......")
            await asyncio.sleep(5)
            
    except Exception as e:
        print(f"Anslutningsfel: {e}")
    finally:
        await client.disconnect()




# Tips för din HTML-dashboard

# Eftersom du bygger en dashboard för detta, kan det vara smart att programmera in en färgindikator för "Differensen":
# 
#     GRÖN (0 - 50 mV): Allt är perfekt.
# 
#     GUL (51 - 100 mV): Ok, men systemet jobbar med balansering.
# 
#     RÖD (> 100 mV): Varning, obalans eller en cell som börjar bli dålig/full mycket snabbare än de andra.
