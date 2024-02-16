import time
import requests
import json

output_json_folder = r"C:\Users\bputra\OneDrive - ESRI Indonesia\PT ESRI Indonesia\Research\code-script\16_bhumi_atrbpn\data"

for req1 in range(250, 260):
    for req2 in range(240, 250):
        url = f'https://bhumi.atrbpn.go.id/bhumigs/umum/wms?version=1.1.1&request=GetFeatureInfo&info_format=application/json&layers=umum:ZNTRANGE&CRS=EPSG:4326&width=1920&height=719&x={req1}&y={req2}&bbox=106.7944325208885,-6.2716550023889965,106.83795382073515,-6.255454471281453&query_layers=umum:ZNTRANGE&srs=EPSG:4326'
        
        response = requests.get(url)
        
        if response.status_code == 200:
            output_json = response.json()

            # Create a unique file name based on req1 and req2
            output_file_path = f"{output_json_folder}\\req1_{req1}_req2_{req2}.json"

            # Write the formatted JSON to the file
            with open(output_file_path, 'w') as output_file:
                json.dump(output_json, output_file, indent=2)

            print(f"JSON response for req1={req1}, req2={req2} written to {output_file_path}")
            time.sleep(1)
        else:
            print(f"Failed to fetch data for req1={req1}, req2={req2}. Status code: {response.status_code}")
