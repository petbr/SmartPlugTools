
"""
    Tar en hex-sträng, kollar de första 4 tecknen (MSB + LSB).
    Returnerar (värde, error).
+"""
#from byteFocused import *

dbgPrintPettra  = False
  
def dPrint(str):
    global dbgPrintPettra
    
    if dbgPrintPettra == True:
        print(str)



def posToKnownFeature(i):
    if i == pos_cycleCounter:
        s = "Cycle counter"
    elif i == pos_SOC:
        s = "SOC"
    elif i == pos_temperature:
        s = "Temperature"
    elif i == pos_v1:
        s = "Voltage U1(V)"
    elif i == pos_v2:
        s = "Voltage U2(V)"
    elif i == pos_v3:
        s = "Voltage U3(V)"
    elif i == pos_v4:
        s = "Voltage U4(V)"
    else:
        s = "?"
        
    return s
    
    
def hex_to_uint16(hexStr):
    dPrint(f"hex_to_uint16({hexStr})")
    if len(hexStr) < 4:
        return 0

    dPrint(f"hex_to_uint16({hexStr[:4]})")

    try:
        # Ta bara de första 4 tecknen
        target = hexStr[:4]
        # Konvertera till osignerat heltal (0 till 65535)
        val = int(target, 16)
        return val
    except ValueError:
        return 0


def hex_to_int16(hexStr):
    dPrint(f"hex_to_int16({hexStr})")
    if len(hexStr) < 4:
        return 0

    try:
        val = int(hexStr, 16) & 0xFFFF

        dPrint(f"Pettra::hex_to_int16, hex_str = {hexStr}, val = {val}")

        # Om talet är större än 32767 (0x7FFF), är det negativt
        if val > 0x7FFF:
            val -= 0x10000 # Dra bort 65536 för att få det negativa värdet
        return val
    except ValueError:
        return 0


def hexWrapped_to_uint16(hex_str):
    """
    Tar en hex-sträng, kollar de första 4 tecknen (MSB + LSB).
    Returnerar (värde, error).
    """
    #print(f"Pettra::hexWrapped_to_uint16, hex_str = {hex_str}")
    if len(hex_str) < 4:
        #print(f"Pettra::hexWrapped_to_uint16, len < 4!!!!!!!!!")
        return 0, "Strängen är för kort, kräver minst 4 tecken"
    
    try:
        # Ta bara de första 4 tecknen
        t01 = hex_str[2:4]
        t23 = hex_str[0:2]
        targetWrapped = f"{t01}{t23}"
        #print(f"Pettra::hexWrapped_to_uint16, t01={t01}, t23={t23}    = {targetWrapped}")
        
        # Konvertera till osignerat heltal (0 till 65535)
        val = int(targetWrapped, 16)
        return val, targetWrapped, None
    except ValueError:
        return 0, "0000", f"Ogiltig hex-sträng: {hex_str[:4]}"
        


def calc_Uint16_HexStr_Temp(h):
        dPrint(f"calc_Uint16_HexStr_Temp({h})")
        ui16, hexStr, _ = hexWrapped_to_uint16(h)        
        decTempValue, _ = calcTemp(ui16)
        dPrint(f"calc_Uint16_HexStr_Temp, ui16 = {ui16}, hexStr = {hexStr},    decTempValue={decTempValue}")
        return ui16, hexStr, decTempValue


def showDifferentValue(hexStr):
    #print(f"Pettra::showDifferentValue()")
    if len(hexStr) < 4:
        dPrint(f"Pettra::showDifferentValue()   <4")
        return 0, None
        
    #print(f"Pettra::showDifferentValue({hexStr[:4]})")
    
    try:
        # Ta bara de första 4 tecknen
        target = hexStr[:4]
        # Konvertera till osignerat heltal (0 till 65535)
        val, _ = hex_to_uint16(hexStr)
        #print(f"Pettra::showDifferentValue,    val = {val}")
        return val, None
    except ValueError:
        return 0, None
    
    
def showTemp(hexStr):
	dPrint(f"showTemp() BEGIN")

	posTempMsb=2
	posTempLsb=0
	
	cTempMsb = hexStr[posTempMsb:posTempMsb+2]
	valTempMsb = int(cTempMsb, 16)
	dPrint(f"cTempMsb=[{cTempMsb}], valTempMsb={valTempMsb}")

	
	cTempLsb = hexSTr[posTempLsb:posTempLsb+2]
	valTempLsb = int(cTempLsb, 16)
	dPrint(f"cTempLsb=[{cTempLsb}], valTempLsb={valTempLsb}")
	
	dPrint(f"showTemp() END")
	return
	
def calcTemp(uint16value):
    dPrint(f"calcTemp({uint16value})")
    decValue = (uint16value / 10.0) - 273.15
    dPrint(f"Temp({uint16value} = {decValue}")
    return decValue, None


def calcAnalog16bit(h):      
    try:
        av = int(h, 16) / 1000
    except ValueError:
        av = 0.0

    dPrint(f"calcAnalog16bit({h}) = {av}")

    return av        

def calcAnalog16bitFromSignedHex(h):      
    dvS = hex_to_int16(h)
    try:
        av = dvS / 1000.0
    except ValueError:
        av = 0.0

    dPrint(f"calcAnalog16bitFromSignedHex({h}) = {av}")

    return av
        

def calcDigital16bit(h):        
    try:
        dv = int(h, 16)
    except ValueError:
        dv = 0

    return dv

def calcMinMax(v1, v2, v3, v4):
    cells = [v1, v2, v3, v4]
    total_V = round(sum(cells), 2)
    diff_mV = (max(cells) - min(cells)) * 1000
    diff_mV = round(diff_mV, 1)
    
    return total_V, diff_mV

def validate_and_parse(frame):
   
    frame = frame.upper().strip()

    for i in range(0, 160, 1):
        dPrint(f"M[{i}-{i+1}]    ={frame[i]}{frame[i+1]},   {frame[i:i+4]} SD={showDifferentValue(frame[i:])}")
        showTemp(frame[i:])

    # Sök efter SOC-markör (63) och Cykel-markör (35) från position 10
    start_search = 10
    pos_DB80 = frame.find("DB80")
    dPrint(f"pos_DB80={pos_DB80}   Pettra was here!")
    frameDB80 = frame[pos_DB80:]
    dPrint(f"pos_DB80={pos_DB80}   Pettra was here!")

    pos_cycle_marker = 6
    pos_soc_marker = 10

    dPrint(f"Cycle counter = {hex_to_uint16(frameDB80[pos_cycle_marker:])}")
    dPrint(f"SOC           = {hex_to_uint16(frameDB80[pos_soc_marker:])}")

    # Validera att de finns på jämna positioner
    #is_valid_soc = pos_soc_marker != -1 and pos_soc_marker % 2 == 0
    #is_valid_cyc = pos_cycle_marker != -1 and pos_cycle_marker % 2 == 0

    if pos_DB800 != -111:


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
    
    # Om vi inte hittar markörerna men har mycket data, skriv ut lite för manuell koll
    elif len(frame) > 150:
        print(f"Söker fortfarande... Buffer-längd: {len(frame)}")




if __name__ == "__main__":
    values ={"0000", "FF00", "00FF", "1234", "ssss", "hhhhhh"}
    for v in values:        
        print(f"\n\nv = {v}")
        v_showDifferentValue, _ = showDifferentValue(v)
        print(f"showDifferentValue() = {v_showDifferentValue}")



