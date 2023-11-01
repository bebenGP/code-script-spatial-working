import requests
import csv

# Define the base URL for the API
base_url = "https://pergikuliner.com/api/restaurants/"

# Define the output directory and CSV file path
output_directory = r"D:\Magang ESRI\JOB\Collect data\Resto"
csv_file_path = f"{output_directory}\\restaurant_data.csv"

# Define the headers for the CSV file
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


# Initialize the list to store scraped data
scraped_data = []

# Loop through ID numbers from 1 to ...
for id_number in range(1, 21):
    url = base_url + str(id_number)

    # Set the authorization token and headers
    headers = {
        'Authorization': 'Token token=M2Y0ODI4ZDZmNzM5ZmIzNjM4N2QwYjk4NmZlMzlhZjMsIDE2OTA4MDg4OTI=',
        'Cookie': 'AWSELB=01E129991AF70BA2C1982EA35EEC711555FED64E414035E0278BBCBF0FB52E910C62AC6F3BA25218FA77E626150EEFCBF2CCCF99AE445473BE794760D430DCA47DAA4201D5; AWSELBCORS=01E129991AF70BA2C1982EA35EEC711555FED64E414035E0278BBCBF0FB52E910C62AC6F3BA25218FA77E626150EEFCBF2CCCF99AE445473BE794760D430DCA47DAA4201D5; _mkra_ctxt=5cad332c3289c787c163ecc2f7868958--200; _session_id=ab7b5b590d853ab6b7cd8ae59d75eeec'
    }

    # Send the GET request to the API
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json().get("restaurant")
        scraped_data.append(data)
        print(f"Scraped data for ID {id_number} successfully.")
    else:
        print(f"Failed to scrape data for ID {id_number}.")

# Save the scraped data to a CSV file with semicolon (;) as delimiter
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    # Change the delimiter to semicolon (;)
    writer = csv.DictWriter(csvfile, fieldnames=csv_headers, delimiter=';')
    writer.writeheader()
    writer.writerows(scraped_data)

print("Scraping and CSV file creation completed successfully.")
