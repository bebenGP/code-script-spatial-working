import requests
import csv
import time

# URL untuk mengambil data
base_url = "https://www.oyorooms.com/api/pwa/nearbyplaces?additional_fields=point_of_interests&filters%5Bhotel_ids%5D="

# Tentukan nama file CSV
output_folder = r"C:\PT ESRI Indonesia\Research\code-script\13_oyo\testing_task_scheduler"
csv_file = f"{output_folder}\\beben_oyo_data_testing10.csv"


# Tulis data ke dalam file CSV
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    
    # Tulis header
    writer.writerow(["source", "id", "name", "latitude", "longitude", 
                    "distance", "categories", 'subcategories', 
                    'oyo_id', 'address', 'hotel_type'
                    ])
            
    for id_hotel in range (88150 , 88200) :
        print('Data :', id_hotel)
        start_time  = time.time()
        
        if id_hotel in (10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000) :
            time.sleep(1800)
        
        url = base_url + str(id_hotel)
        # Ambil data dari URL
        header = {      
                'Sec-Ch-Ua' : '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
                'Sec-Ch-Ua-Mobile' : '?0',
                'Sec-Ch-Ua-Platform' : '"Windows"',
                'Sec-Fetch-Dest' : 'empty',
                'Sec-Fetch-Mode' : 'cors',
                'Sec-Fetch-Site' : 'same-origin',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                'Xsrf-Token' : 'wv3D3Mhr-whZzCCMb-wvI3DPM5hgwMFboMQk'
            }
                
        response = requests.get(url, headers=header)
        
        try : 
            data = response.json()

            # Ambil request_id
            request_id = data["request_id"]

            # Ambil array hotels
            hotels = data.get("hotels", [])

            # Ambil poin minat dari setiap hotel
            point_of_interests = []
            for hotel in hotels:
                point_of_interests.extend(hotel.get("point_of_interests", []))
            
            # Tulis data point_of_interests
            for poi in point_of_interests:
                poi_id = poi.get("id", "")
                poi_name = poi.get("name", "")
                poi_latitude = poi.get("latitude", "")
                poi_longitude = poi.get("longitude", "")
                poi_distance = poi.get("distance", "")
                poi_categories = poi.get("categories", "")
                poi_subcategories = poi.get("sub_categories","")
                
                writer.writerow(["point_of_interests", poi_id, poi_name, poi_latitude, 
                                poi_longitude, poi_distance, poi_categories, 
                                poi_subcategories, "", "", ""])

            # Tulis data hotels
            for hotel in hotels:
                longitude = hotel.get("longitude", "")
                latitude = hotel.get("latitude", "")
                id = hotel.get("id", "")
                oyo_id = hotel.get("oyo_id", "")
                category = hotel.get("category", "")
                name = hotel.get("name", "")
                address = hotel.get("address", "")
                hotel_type = hotel.get("hotel_type", "")
                
                writer.writerow(["hotels", id, name, 
                                latitude, longitude, "", 
                                category, "", oyo_id, 
                                address, hotel_type])
        except KeyError :
            print("Yaudah lah ya, ada error skip aee")       
        
        end_time = time.time()
        elapsed_time = end_time - start_time        
        print(f"Waktu yang dibutuhkan: {elapsed_time} detik")
        
        time.sleep(5)
        
        
    print(f"Data telah ditulis ke {csv_file}.")
