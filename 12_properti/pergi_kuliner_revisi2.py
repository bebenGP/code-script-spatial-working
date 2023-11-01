import requests
import csv
import time
import re

base_url = "https://pergikuliner.com/api/restaurants/"
output_directory = r"C:\Users\beben\Documents\Scrapping Research\output_pergi_kuliner\lanjutan_tahap_2"
csv_file_path = f"{output_directory}\\restaurant_data_testing40.csv"

csv_headers = ["id", "name", "is_chain", "address", "region", "area", "phone", "website", "average_price",
               "regional_food", "kind", "cuisine_type", "operating_hour", "payment", "has_delivery",
               "has_parking_area", "has_vip_room", "has_wifi", "need_reservation", "has_outdoor_seat",
               "has_halal_certification", "number_of_seat", "information", "latitude", "longitude",
               "is_approved", "is_published", "rate_average", "permalink", "is_recommended",
               "has_smoking_area", "has_alcohol", "is_full_time", "has_vegetarian", "email", "is_closed",
               "city", "greater_area", "building_name", "chain_name", "weighted_score", "open_date",
               "close_date", "rate_rasa", "rate_suasana", "rate_harga", "rate_pelayanan", "rate_kebersihan",
               "link_to", "famous_food", "is_wishlist", "promotional_text", "start_date_renovation",
               "promotions_empty?", "is_open_now", "is_official", "menu_items_recommended", "category",
               "end_date_renovation", "is_under_renovation", "main_image", "is_move", "images", "short_url",
               "menus_empty?", "gallery_status", "recommended_dishes", "nearest_stations", "gallery_status"]

## Untuk memberi batas : jika 10 kali berturut - turut error maka script akan dihentikan 
maksimal_error_failed = 20  # Maximum consecutive failures allowed
tracking_error_failed = 0

## Script dan logika berjalan langsung di modul csv
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_headers, delimiter=',')
    writer.writeheader()

    #Memulai hit api dari urutan ke ---
    for id_number in range(118645, 148671):
        
        #kasih delay
        time.sleep(10)
        
        #batasan error
        if tracking_error_failed >= maksimal_error_failed:
            print(f"Melebihi batas maksimum failed ({maksimal_error_failed}). Exiting the script.")
            break
        
        ##########################################################################Untuk Authorization####################################################################
        
        url = "https://pergikuliner.com"

        response = requests.get(url)
        page_content = response.text

        # Define the regex pattern to match the Authorization token within beforeSend function
        pattern = r"xhr\.setRequestHeader\('Authorization', \"(Token token=[^\"]+)\"\)"

        # Use regex to find the token
        match = re.search(pattern, page_content)

        if match:
            token = match.group(1)
            print(f"ID {id_number} Token didapatkan: {token}")
        else:
            print("Authorization Token not found.")
        
        url = base_url + str(id_number)
        headers = {
            'Authorization': f'{token}',
            'Cookie': 'AWSELB=01E129991AF70BA2C1982EA35EEC711555FED64E414035E0278BBCBF0FB52E910C62AC6F3BA25218FA77E626150EEFCBF2CCCF99AE445473BE794760D430DCA47DAA4201D5; AWSELBCORS=01E129991AF70BA2C1982EA35EEC711555FED64E414035E0278BBCBF0FB52E910C62AC6F3BA25218FA77E626150EEFCBF2CCCF99AE445473BE794760D430DCA47DAA4201D5; _mkra_ctxt=5cad332c3289c787c163ecc2f7868958--200; _session_id=ab7b5b590d853ab6b7cd8ae59d75eeec'
        }

        ##########################################################################Untuk Authorization####################################################################


        ## Menulis Output
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json().get("restaurant")
            if "is_cashless_only" in data:
                del data["is_cashless_only"]
            writer.writerow(data)
            print(f"Scraped data ID {id_number} ... Berhasil !!!")
            tracking_error_failed = 0  # Reset tracking error
        else:
            tracking_error_failed += 1
            print(f"Failed scrape data, ID {id_number}. Failed sebanyak : {tracking_error_failed}")

        ## Finish !!!
print("Scraping data sudah selesai")