
import requests
import json
import time


# Inställningar
KEY_NAME = "Key: "

ACCOUNT_ID   = os.getenv("ACCOUNT_ID")
NAMESPACE_ID = os.getenv("NAMESPACE_ID")
API_TOKEN    = os.getenv("API_TOKEN")
KEY_NAME     = os.getenv("KEY_NAME")

# BATTERY_STORAGE, ID = 28c3ca0c80fd44e78fda558d7e5ed553
# "battproj.pages.dev"
# "PB_WorkersReadWrite"
# "current_bms_data"



battHtml = """
<!DOCTYPE html>
<html lang="sv"><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BMS Dashboard</title>
    <style>
        :root {
            --bg-color: #121212;
            --card-bg: #1e1e1e;
            --text-main: #ffffff;
            --text-dim: #b0b0b0;
            --accent: #00e676; /* Grön */
            --warning: #ffab00; /* Gul/Orange */
            --danger: #ff5252;  /* Röd */
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .container {
            max-width: 1000px;
            width: 100%;
        }

        header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 1px solid #333;
            padding-bottom: 10px;
        }

        /* Grid Layout */
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }

        .card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }

        h2 { font-size: 1rem; color: var(--text-dim); margin-top: 0; text-transform: uppercase; letter-spacing: 1px; }

        /* Batteri-visualisering */
        .battery-section {
            display: flex;
            align-items: center;
            justify-content: space-around;
        }

        .battery-body {
            width: 80px;
            height: 140px;
            border: 4px solid #444;
            border-radius: 8px;
            position: relative;
            padding: 4px;
        }

        .battery-body::after {
            content: '';
            position: absolute;
            top: -12px;
            left: 25%;
            width: 50%;
            height: 8px;
            background: #444;
            border-radius: 4px 4px 0 0;
        }

        .battery-level {
            width: 100%;
            background: var(--accent);
            position: absolute;
            bottom: 4px;
            left: 0;
            right: 0;
            border-radius: 2px;
            transition: height 0.5s ease;
            /* Dynamisk färg baserat på SOC kan skötas via Python/Inlinestyles */
        }

        /* Cell-staplar */
        .cell-container {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            height: 120px;
            padding-top: 20px;
        }

        .cell-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 20%;
        }

        .cell-bar {
            width: 100%;
            background: #2196f3;
            border-radius: 4px 4px 0 0;
            min-height: 2px;
        }

        .cell-val { font-size: 0.8rem; margin-top: 8px; }

        /* Stora värden */
        .big-value { font-size: 2.5rem; font-weight: bold; margin: 10px 0; }
        .unit { font-size: 1rem; color: var(--text-dim); }

        .data-row {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding-bottom: 5px;
            border-bottom: 1px solid #2a2a2a;
        }

        .label { color: var(--text-dim); }
    </style>
</head>
<body>

<div class="container">
    <header>
        <h1>BMS Status - Batteripaket 1</h1>
        <p style="color: var(--text-dim)">First version: 2026-05-01 14:35:12</p>
    </header>

    <div class="dashboard-grid">
        
        <!-- Laddning & Kapacitet -->
        <div class="card">
            <h2>State of Charge</h2>
            <div class="battery-section">
                <div class="battery-body">
                  <!-- Python: sätt height till SOC% och byt färg om < 20 -->
                  <div class="battery-level" style="height: 65%; background: var(--accent);background-color: #ff0000;">
		  </div>
                </div>
                <div>
                    <div class="big-value">25 <span class="unit">%</span></div>
                    <div class="label">Kapacitet: 81.7 / 98.5 Ah</div>
                </div>
            </div>
        </div>

        <!-- Systemhälsa -->
        <div class="card">
            <h2>Systemdata</h2>
            <div class="data-row">
                <span class="label">Total Spänning</span>
                <span><strong>13.55 V</strong></span>
            </div>
            <div class="data-row">
                <span class="label">Ström</span>
                <span><strong>okänt A</strong></span>
            </div>
            <div class="data-row">
                <span class="label">Temperatur</span>
                <span style="color: var(--accent)"><strong>14.5 °C</strong></span>
            </div>
            <div class="data-row">
                <span class="label">Cykler</span>
                <span>432 / 10000</span>
            </div>
            <div class="data-row">
                <span class="label">Celldiff</span>
                <span style="color: var(--warning)">0.012 V</span>
            </div>
        </div>

        <!-- Cellspänning Visualisering -->
        <div class="card" style="grid-column: span 1;">
            <h2>Cellbalans (0-5V)</h2>
            <div class="cell-container">
                <!-- Python: Räkna ut höjd i % (Volt / 5 * 100) -->
		<div class="cell-wrapper" style="display: flex; flex-direction: column; align-items: center; width: 70px;">
    			<!-- Själva stapeln -->
    			<div class="cell-bar" style="
        			height: 26px; 
        			width: 20px; 
        			background-color: #2196f3; 
        			border-radius: 4px 4px 0 0;
        			border: 1px solid #1565c0;">
    			</div>
    
			<!-- Texten under -->
			<span class="cell-val" style="color: white; font-size: 0.8rem; margin-top: 5px;">u1=3.31V</span>
		</div>

		<div class="cell-wrapper" style="display: flex; flex-direction: column; align-items: center; width: 70px;">
    			<!-- Själva stapeln -->
    			<div class="cell-bar" style="
        			height: 66px; 
        			width: 20px; 
        			background-color: #2196f3; 
        			border-radius: 4px 4px 0 0;
        			border: 1px solid #1565c0;">
    			</div>
    
			<!-- Texten under -->
			<span class="cell-val" style="color: white; font-size: 0.8rem; margin-top: 5px;">u2=3.1V</span>
		</div>

		<div class="cell-wrapper" style="display: flex; flex-direction: column; align-items: center; width: 70px;">
    			<!-- Själva stapeln -->
    			<div class="cell-bar" style="
        			height: 66px; 
        			width: 20px; 
        			background-color: #2196f3; 
        			border-radius: 4px 4px 0 0;
        			border: 1px solid #1565c0;">
    			</div>
    
			<!-- Texten under -->
			<span class="cell-val" style="color: white; font-size: 0.8rem; margin-top: 5px;">u3=3.21V</span>
		</div>

		<div class="cell-wrapper" style="display: flex; flex-direction: column; align-items: center; width: 70px;">
    			<!-- Själva stapeln -->
    			<div class="cell-bar" style="
        			height: 99px; 
        			width: 20px; 
        			background-color: #2196f3; 
        			border-radius: 4px 4px 0 0;
        			border: 1px solid #1565c0;">
    			</div>
    
			<!-- Texten under -->
			<span class="cell-val" style="color: white; font-size: 0.8rem; margin-top: 5px;">u4=3.31V</span>
		</div>



            </div>
        </div>

    </div>
</div>
</body></html>

"""


def update_cloudflare_kv(keyId, value_string):
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/storage/kv/namespaces/{NAMESPACE_ID}/values/{KEY_NAME}{keyId}"
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "text/plain" # Eller "application/json" om du skickar JSON
    }

    print(f"\nurl={url}\n")
    print(f"\nheaders={headers}\n")
    print(f"\nvalue_string={value_string}\n")
    print(f"\nkeyId={keyId}\n")
    
    try:
        response = requests.put(url, headers=headers, data=value_string)
        
        if response.status_code == 200:
            print("Successfully updated Cloudflare KV!")
        else:
            print(f"Failed to update. Status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")

# Exempel på användning med din batteridata
# Du kan skicka hela din textrad här
my_data = "SOC:85%,Temp:24.5,V:13.2"
#update_cloudflare_kv(my_data)
update_cloudflare_kv("KeyNo318", battHtml)

time.sleep(60)

#import json

# Skapa ett dictionary med dina värden
batt_dict = {
    "soc": 85,
    "temp": 24.5,
    "total_v": 13.2,
    "cells": [3.585, 3.608, 3.606, 3.597],
    "misc": "Kilroy was here, 2026-05-16 07:51"
}

# Gör om till JSON-sträng och skicka
#update_cloudflare_kv(json.dumps(batt_dict))
update_cloudflare_kv("KeyNo319", battHtml)



#1      SOC:85%,Temp:24.5,V:13.2
#2      
#{"soc": 85, "temp": 24.5, "total_v": 13.2, "cells": [3.585, 3.608, 3.606, 3.597], "misc": "Kilroy was here, 2026-05-16 07:51"}















