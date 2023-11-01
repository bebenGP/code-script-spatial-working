# -*- coding: utf-8 -*-
import urllib3,json,csv,os,traceback,time



inputFile=r"C:\PT ESRI Indonesia\Project\P2 (Data Services)\Scraping Data\Fixed\RAW_Data_ATM_Mandiri_fix.csv"
outputFile=r"C:\PT ESRI Indonesia\Project\P2 (Data Services)\Scraping Data\Fixed\output_geocoding_mandiri_testing.csv"
inputPOINameField="brand"
inputAddressField="address"
csvDelimiter=','

start=-1

def mintaWaze(alamat2an,line):
    #wazeURL="https://gapi.waze.com/autocomplete/q?q={}&e=ALL&c=web&lang=en".format(alamat2an)
    wazeURL= "https://www.waze.com/live-map/api/autocomplete/?q={}&exp=8%2C10%2C12&sll=-4.929928176802042%2C116.72764393551184&lang=id".format(alamat2an)
    http = urllib3.PoolManager()
    response = http.request('GET', wazeURL)
    data = response.data.decode('ascii', 'ignore')
    test=json.loads(data)
    #print test
    
    time.sleep(7)
    
    for something in test:
        try:
            ############################ 2.7
            alamat=something['address'].encode('ascii', 'ignore').decode('ascii', 'ignore')
            if alamat not in line:
                line.append(something['cleanName'].encode('ascii', 'ignore').decode('ascii', 'ignore'))
                line.append(alamat.encode('ascii', 'ignore').decode('ascii', 'ignore'))
                line.append(something['latLng']['lng'])
                line.append(something['latLng']['lat'])
        except Exception:
            print(something)
            traceback.print_exc()
    return line

############################ 3.x
##input_file = csv.DictReader(open(inputFile,encoding='utf-8'))
##with open(outputFile, "a+",encoding='utf-8') as csv_file:
##    csvWriter = csv.writer(csv_file, delimiter=csvDelimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect='unix')
############################

############################ 2.7
input_file = csv.DictReader(open(inputFile))
with open(outputFile, "ab+") as csv_file:
    csvWriter = csv.writer(csv_file, delimiter=csvDelimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
############################
    headers = input_file.fieldnames
    newHeaders=list(headers)
    for x in range(5):
        newHeaders.append('cleanName')
        newHeaders.append('address')
        newHeaders.append('lng')
        newHeaders.append('lat')
    newHeaders.append('...')
    #print headers
    #print newHeaders
    if os.stat(outputFile).st_size == 0:
        csvWriter.writerow(newHeaders)
    print("processing...")
    for idx,row in enumerate(input_file):
        if idx%100==0 and idx>0: 
            print("{} done".format(idx))
        if idx>start:
            line=[]
            for col in headers:
                line.append(row[col].decode('ascii', 'ignore'))
            fullAddress1=row[inputPOINameField].decode('ascii', 'ignore').replace("#","").strip()+" "+row[inputAddressField].decode('ascii', 'ignore').replace("#","").strip()
            line1=mintaWaze(fullAddress1,line)
            fullAddress1=row[inputPOINameField].decode('ascii', 'ignore').replace("#","").strip()
            line2=mintaWaze(fullAddress1,line1)
            fullAddress1=row[inputAddressField].decode('ascii', 'ignore').replace("#","").strip()
            line=mintaWaze(fullAddress1,line2)
            csvWriter.writerow(line)
    print("finished")
