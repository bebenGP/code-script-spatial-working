import pandas as pd
import urllib3
import json
import csv
import os
import traceback
import time

input_file = r'D:\SCRIPT - ARCPY - PYTHON\script-python-working-in-esri\18_update_version_crawling_waze_ver2.0\input\keyword_req_data_bulutangkis_testing1.csv'
output_file = r'D:\telkomsel-poi\output\get_data_waze2.0_bulutangkis_indonesia_testing1.csv'

df = pd.read_csv(input_file, delimiter=';')

def crawling_data(keyword_data, min_y_data, min_x_data, max_y_data, max_x_data) :
    url = f'https://www.waze.com/live-map/api/autocomplete/?q={keyword_data}&exp=8,10,12&v={min_y_data},{min_x_data};{max_y_data},{max_x_data}&lang=en'
    print(f'start crawling {url}')
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    data = response.data.decode('ascii', 'ignore')
    
    time.sleep(2)
    
    try:
        json_data = json.loads(data)
        return json_data
    except Exception as e:
        print('Error:', e)
        traceback.print_exc()
        return []

# Write data to CSV file
with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['name', 'cleanName', 'address', 'venueId', 'lat', 'lng']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
    
    # Write header
    writer.writeheader()
    try :
        for _, row in df.iterrows():
            try :
                data = crawling_data(keyword_data=row['keyword'], min_y_data=row['min_y'], min_x_data=row['min_x'], max_y_data=row['max_y'], max_x_data=row['max_x'])
                for item in data:
                    lat = item['latLng']['lat']
                    lng = item['latLng']['lng']
                    del item['latLng']
                    item['lat'] = lat
                    item['lng'] = lng
                    writer.writerow(item)
            except Exception as e :
                print(f"Error di function bagian crawling/collect data {e}")
    except Exception as e :
        print(f"Terdapat error {e}")

print("Data sudah selesai di Scrapping !!!", output_file)
