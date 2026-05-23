import asyncio
from PettraHelpers import *

from bleak import BleakClient

ADDRESS = "B0:B1:13:75:11:12"
NOTIFY_UUID = "0000ffe4-0000-1000-8000-00805f9b34fb"

DEBUG = True  # Ändra till False när du är nöjd
is_parsing = False    # Global flagga
buffer = ""

pos_cycleCounter = 6
pos_SOC          = 10
pos_temperature  = 16
pos_v1           = 30
pos_v2           = 34
pos_v3           = 38
pos_v4           = 42
dbgPrinting      = True
#dbgPrinting      = False

def KalleshowDifferentValue(hexStr):
    print(f"showDifferentValue()")
    if len(hexStr) < 4:
        print(f"showDifferentValue()   <4")
        return 0
        
    print(f"showDifferentValue({hexStr[:4]})")
    
    try:
        # Ta bara de första 4 tecknen
        target = hexStr[:4]
        # Konvertera till osignerat heltal (0 till 65535)
        val = hex_to_uint16(hexStr)
        return val
    except ValueError:
        return 0






def extraText(i, h):
    global pos_cycleCounter
    global pos_SOC
    global pos_temperature
    
    if i == pos_cycleCounter:
        extraText = "  CycleCounter"
    elif i == pos_SOC:
        extraText = "  SOC"
    elif i == pos_temperature:
        extraText = "  Temperature"
    elif i == pos_v1:
        v1 = calcAnalog16bit(h)
        extraText = f"  v1={v1}V"
    elif i == pos_v2:
        v2 = calcAnalog16bit(h)
        extraText = f"  v2={v2}V"
    elif i == pos_v3:
        v3 = calcAnalog16bit(h)
        extraText = f"  v3={v3}V"
    elif i == pos_v4:        
        v4 = calcAnalog16bit(h)
        extraText = f"  v4={v4}V"
    else:
        try:
            c = int(h, 16) / 1000
            extraText = f"        current = {c}, h={h}" 
        except ValueError:
            c = 0
            extraText = "----bad characters----"
        
    return extraText


def validate_and_parse(frame):
    global pos_cycleCounter
    global pos_SOC
    global pos_temperature
    
    lFrame = frame.upper().strip()
    #lFrame = frame.upper()

    print(f"validate_and_parse(), is_parsing = {is_parsing}")
    
    pos_DB80 = lFrame.find("DB80")
    if pos_DB80 != -1:
        print(f"validate_and_parse(), FOUND DB80!!!!!!     pos_DB80 = {pos_DB80}")
    else:
        print(f"validate_and_parse(), didn't find DB80\n{lFrame}")
        return

    db80Frame = lFrame[pos_DB80:]
    frame = ""
    print(f"validate_and_parse(), db80Frame = {db80Frame}")
    print(f"pos_cycleCounter = {pos_cycleCounter}")
    print(f"pos_SOC          = {pos_SOC}")
    print(f"pos_temperature  = {pos_temperature}")
    print(f"pos_v1  = {pos_v1}")
    print(f"pos_v2  = {pos_v2}")
    print(f"pos_v3  = {pos_v3}")
    print(f"pos_v4  = {pos_v4}")


    for i in range(0, 100, 2):
        h = db80Frame[i:i+4]
        et = extraText(i, h)   #Until we know better

        print(f"i = {i:03}, h  = [{h}]{et}")
    
    print(f"\n")

    cycle_CounterStr = db80Frame[pos_cycleCounter:pos_cycleCounter+4]
    SOC_Str          = db80Frame[pos_SOC:pos_SOC+4]
    temp_Str         = db80Frame[pos_temperature:pos_temperature+4]
    v1_Str           = db80Frame[pos_v1:pos_v1+4]
    v2_Str           = db80Frame[pos_v2:pos_v2+4]
    v3_Str           = db80Frame[pos_v3:pos_v3+4]
    v4_Str           = db80Frame[pos_v4:pos_v4+4]
    
    print(f"cycle_CounterStr = {cycle_CounterStr}")
    print(f"SOC_Str          = {SOC_Str}")
    print(f"temp_Str         = {temp_Str}")
    print(f"v1_Str           = {v1_Str}")
    print(f"v2_Str           = {v2_Str}")
    print(f"v3_Str           = {v3_Str}")
    print(f"v4_Str           = {v4_Str}")

    print(f"cycle")
    ui16_Cycle_Counter, _    = hex_to_uint16(cycle_CounterStr)
    print(f"SOC")
    ui16_SOC_Counter, _      = hex_to_uint16(SOC_Str)
    print(f"Temp")
    _, _, temp               = calc_Uint16_HexStr_Temp(temp_Str)
    temp                     = round(temp,1)
    v1                       = calcAnalog16bit(v1_Str)
    v2                       = calcAnalog16bit(v2_Str)
    v3                       = calcAnalog16bit(v3_Str)
    v4                       = calcAnalog16bit(v4_Str)
    total_V, diff_mV         = calcMinMax(v1, v2, v3, v4)
    print(f"--------- ui16_Cycle_Counter: {ui16_Cycle_Counter}")
    print(f"--------- ui16_SOC_Counter  : {ui16_SOC_Counter}")
    print(f"--------- Temperature       : {temp}")
    print(f"--------- v1                : {v1}")
    print(f"--------- v2                : {v2}")
    print(f"--------- v3                : {v3}")
    print(f"--------- v4                : {v4}")
    print(f"--------- vTotal            : {total_V}V")
    print(f"--------- Diff:             : {diff_mV}mV")
    
    

    return
    # Sök efter SOC-markör (63) och Cykel-markör (35) från position 10
    start_search = 10
    debugPrint(dbg, f"pos_DB80={pos_DB80}   Pettra was here!")
    frameDB80 = lFrame[pos_DB80:]
    print(f"pos_DB80={pos_DB80}   Pettra was here!")





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
    








def callback(sender, data):
    global buffer
    global is_parsing
    #global dbgPrinting
    
    if dbgPrinting == True:
        print(f"callback()!!!\nsender={sender}\ndata={data}     When debugging!")
        
    print(f"callback()!!!\nsender={sender}\ndata={data}         Unconditionally")
        
    chunk = data.decode('ascii', errors='ignore')
    buffer += chunk
    print(f"size of buffer = {len(buffer)}\nbuffer={buffer}\n\n")
    
    # Vi väntar tills vi har ett rejält block innan vi analyserar
    #print(f"Buffer len = {len(buffer)}")                
    if len(buffer) > 230:
        if is_parsing:
            print("callback(), parsing.......do nothing!")
            returned_value
        
        try:
            is_parsing = True                
            sendBuffer = buffer
            buffer = ""
            print(f"\n\n>230, Call validate_and_parse......BEGIN, len(buffer)={len(sendBuffer)}")                    
            validate_and_parse(sendBuffer)
            print(f"Call validate_and_parse......END")
        finally:
            is_parsing = False  # Now finished and can retrieve next chunk


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
            print(f"await asyncio.sleep(10)......")
            await asyncio.sleep(10)
            print(f"...asyncio.sleep(10) READY!")
            
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
