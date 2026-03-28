import asyncio
from kasa.iot import IotPlug
from datetime import datetime
# Inställningar
DEVICE_IP_Testing = "192.168.1.160"  # Ändra till din pluggs IP
DEVICE_IP_Drainpump = "192.168.1.160"  # Ändra till din pluggs IP

# Use testing device until FINAL version
DEVICE_IP = DEVICE_IP_Testing

async def monitor_and_control():
    # Initiera pluggen
    plug = IotPlug(DEVICE_IP)
    plugState : bool
    plugState = True
    
    
    try:
        while True:
            # Uppdatera all data från pluggen (Energimätning + Status)
            await plug.update()
                    
            # Hämta alla modules
            allModules = plug.modules
            # print(f"all_modules:          {allModules}")
            
            # all_modules: 'Energy', 'schedule', 'usage', 'anti_theft', 'Time', 'cloud'            
            energyData     = allModules['Energy'].data
            scheduleData   = allModules['schedule'].data
            usageData      = allModules['usage'].data
            anti_theftData = allModules['anti_theft'].data
            timeData       = allModules['Time'].data
            cloudData      = allModules['cloud'].data
            """
            print(f"energyData:     {energyData}\n")
            print(f"scheduleData:   {scheduleData}\n")
            print(f"usageData:      {usageData}\n")
            print(f"anti_theftData: {anti_theftData}\n")
            print(f"timeData:       {timeData}\n")
            print(f"cloudData:      {cloudData}\n")             """


            # Hämta den råa realtime datan
            realtimeData = energyData['get_realtime']

            # Räkna om från milli till standardenheter
            voltage  = realtimeData['voltage_mv'] / 1000  # Volt
            current  = realtimeData['current_ma'] / 1000  # Ampere
            power    = realtimeData['power_mw'] / 1000    # Watt
            total    = realtimeData['total_wh'] / 1000    # kWh 
            print(f"Spänning:          {voltage} V")
            print(f"Ström:             {current} A")
            print(f"Effekt:            {power} W")
            print(f"Total förbrukning: {total} kWh")            
            
            # Hämta den råa Daystat datan            
            daystat_data  = plug.modules['Energy'].data['get_daystat']
            day_list = daystat_data['day_list']                                              
            # print(f"Day_list           {day_list}")            

            is_on = plug.is_on
            
            # now = timeData
            theTime = timeData['get_time']
            tYear   = theTime['year']
            tMonth  = theTime['month']
            tMday   = theTime['mday']
            tHour   = theTime['hour']
            tMin    = theTime['min']
            tSec    = theTime['sec']
            """ print(f"theTime: {theTime}")            
            print(f"tYear:  {tYear}")            
            print(f"tMonth: {tMonth}")            
            print(f"tMday:  {tMday}")            
            print(f"tHour:  {tHour}")            
            print(f"tMin:   {tMin}")            
            print(f"tSec:   {tSec}")            """

            now = f"{tHour:02}:{tMin:02}:{tSec:02}"
            
            print(f"[{now}] Status: {'PÅ' if is_on else 'AV'} | Effekt: {power:.2f} W | Spänning: {voltage:.1f} V")

            # EXEMPEL PÅ LOGIK (ON/OFF):
            # Om du vill slå av den vid för hög effekt (t.ex. över 2000W i husbilen)
            # if power > 2000:
            #     await plug.turn_off()
            #     print("!!! SÄKERHETSAVSTÄNGNING: För hög last !!!")

            # Vänta 1 sekund innan nästa poll
            await asyncio.sleep(5.0)
            
            print(f"plugState = {plugState}")
            if plugState:
                print("plug OFF")
                await plug.turn_off()
                plugState = False
            else:
                print("plug ON")
                await plug.turn_on()
                plugState = True
            
    except Exception as e:
        print(f"Ett fel uppstod: {e}")

# Funktion för att bara slå PÅ/AV (kan anropas separat)
async def switch_power(state: bool):
    print("switch_power({state})")
    plug = SmartPlug(DEVICE_IP)
    if state:
        await plug.turn_on()
        print("Pluggen är nu PÅ")
    else:
        await plug.turn_off()
        print("Pluggen är nu AV")

if __name__ == "__main__":
    try:
        asyncio.run(monitor_and_control())
    except KeyboardInterrupt:
        print("\nAvbryter övervakning...")


"""
#######################33
# sudo apt update
# sudo apt install pipx
# pipx ensurepath
# kasa --target 192.168.1.255 discover
Success! Added /home/peter/.local/bin to the PATH environment variable.
Consider adding shell completions for pipx. Run 'pipx completions' for instructions.
You will need to open a new terminal or re-login for the PATH changes to take effect.
Otherwise pipx is ready to go!
pipx install python-kasa

kasa --target 192.168.1.255 discover

Install pip
sudo apt install python3-pip

Skapa en mapp och en miljö
mkdir mitt_projekt && cd mitt_projekt
python3 -m venv venv

Aktivera miljön
source venv/bin/activate

Installera biblioteket:
pip install python-kasa


Tillgängliga mätvärden: {
'get_realtime': {'voltage_mv': 234866, 'current_ma': 25, 'power_mw': 1040, 'total_wh': 5, 'err_code': 0},

'get_daystat': 
    {
        'day_list': [
            {'year': 2026, 'month': 3, 'day': 14, 'energy_wh': 2657}, 
            {'year': 2026, 'month': 3, 'day': 15, 'energy_wh': 2651}, 
            {'year': 2026, 'month': 3, 'day': 16, 'energy_wh': 3845}, 
            {'year': 2026, 'month': 3, 'day': 17, 'energy_wh': 1447}, 
..
            {'year': 2026, 'month': 3, 'day': 25, 'energy_wh': 2621}, 
            {'year': 2026, 'month': 3, 'day': 26, 'energy_wh': 3439}, 
            {'year': 2026, 'month': 3, 'day': 27, 'energy_wh': 7494}, 
            {'year': 2026, 'month': 3, 'day': 1, 'energy_wh': 3579}, 
            {'year': 2026, 'month': 3, 'day': 2, 'energy_wh': 3360}, 
            {'year': 2026, 'month': 3, 'day': 3, 'energy_wh': 2266}, 
            {'year': 2026, 'month': 3, 'day': 4, 'energy_wh': 4136}, 
            {'year': 2026, 'month': 3, 'day': 5, 'energy_wh': 5366}, 
            {'year': 2026, 'month': 3, 'day': 6, 'energy_wh': 5539}, 
            {'year': 2026, 'month': 3, 'day': 7, 'energy_wh': 4024}, 
            {'year': 2026, 'month': 3, 'day': 8, 'energy_wh': 2091}, 
            {'year': 2026, 'month': 3, 'day': 9, 'energy_wh': 2350}, 
            {'year': 2026, 'month': 3, 'day': 10, 'energy_wh': 4727}, 
            {'year': 2026, 'month': 3, 'day': 11, 'energy_wh': 2754}, 
            {'year': 2026, 'month': 3, 'day': 12, 'energy_wh': 1392}, 
            {'year': 2026, 'month': 3, 'day': 13, 'energy_wh': 2586}, 
            {'year': 2026, 'month': 3, 'day': 28, 'energy_wh': 1637}], 
        'err_code': 0
    }, 

'get_monthstat': 
    {
        'month_list': [
            {'year': 2026, 'month': 1, 'energy_wh': 379558}, 
            {'year': 2026, 'month': 2, 'energy_wh': 310807}, 
            {'year': 2026, 'month': 3, 'energy_wh': 101051}
        ],
        'err_code': 0}
}
        
Råa värdet:  {'voltage_mv': 234866, 'current_ma': 25, 'power_mw': 1040, 'total_wh': 5, 'err_code': 0}





all_modules:   'Energy', 'schedule', 'usage', 'anti_theft', 'Time', 'cloud'
{'Energy': <Module Emeter (emeter) for 192.168.1.160>, 
 'schedule': <Module Schedule (schedule) for 192.168.1.160>, 
 'usage': <Module Usage (schedule) for 192.168.1.160>, 
 'anti_theft': <Module Antitheft (anti_theft) for 192.168.1.160>, 
 'Time': <Module Time (time) for 192.168.1.160>, 
 'cloud': <Module Cloud (cnCloud) for 192.168.1.160>, 'Led': <Module Led (system) for 192.168.1.160>}

"""
