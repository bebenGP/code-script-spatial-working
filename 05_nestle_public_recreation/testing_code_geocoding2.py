import pandas as pd
import urllib3
import json
import csv
import os
import traceback
import time

inputFile = r"C:\PT ESRI Indonesia\Research\code-script\05_nestle_public_recreation"
outputFile = r"C:\Users\bputra\Documents\script_task\alfamart_indomaret\output\get_data_taman_indonesia_testing3.csv"
inputPOINameField = "site"
inputAddressField = "district"
csvDelimiter = ';'
start = -1
print(inputFile)


def mintaWaze(alamat2an, line):
    wazeURL = "https://www.waze.com/live-map/api/autocomplete/?q={}&exp=8%2C10%2C12&sll=-4.929928176802042%2C116.72764393551184&lang=id".format(
        alamat2an)
    http = urllib3.PoolManager()
    response = http.request('GET', wazeURL)
    data = response.data.decode('ascii', 'ignore')
 
    #delay sekitar (5detik)
    #time.sleep(1)
 
    try:
        test = json.loads(data)
        for something in test:
            
            #time.sleep(1)
            
            try:
                alamat = something['address']
                if alamat not in line:
                    line.append(something['cleanName'])
                    line.append(alamat)
                    line.append(something['latLng']['lng'])
                    line.append(something['latLng']['lat'])
            except Exception:
                print(something)
                traceback.print_exc()
    except json.decoder.JSONDecodeError:
        print("Failed to parse JSON data: {}".format(data))
        traceback.print_exc()
    
    return line


df = pd.read_csv(inputFile, delimiter=csvDelimiter)

with open(outputFile, "a+", newline='', encoding='utf-8') as csv_file:
    csvWriter = csv.writer(csv_file, delimiter=csvDelimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    headers = list(df.columns)
    newHeaders = headers.copy()
    for _ in range(5):
        newHeaders.append('cleanName')
        newHeaders.append('address')
        newHeaders.append('lng')
        newHeaders.append('lat')
    newHeaders.append('...')

    if os.stat(outputFile).st_size == 0:
        csvWriter.writerow(newHeaders)

    print("processing...")
    for idx, row in df.iterrows():
        
        print("Data ke : {}".format(idx))
        print(row)
                
        #Kasih Delay
        #time.sleep(1)
        
        if idx > start:
            line = []
            for col in headers:
                line.append(row[col])
            fullAddress1 = row[inputPOINameField].replace("#", "").strip() + " " + row[inputAddressField].replace("#", "").strip()
            line1 = mintaWaze(fullAddress1, line)
            fullAddress1 = row[inputPOINameField].replace("#", "").strip()
            line2 = mintaWaze(fullAddress1, line1)
            fullAddress1 = row[inputAddressField].replace("#", "").strip()
            line = mintaWaze(fullAddress1, line2)
            csvWriter.writerow(line)
            if idx % 100 == 0 and idx > 0:
                print("{} done".format(idx))

    print("finished")
