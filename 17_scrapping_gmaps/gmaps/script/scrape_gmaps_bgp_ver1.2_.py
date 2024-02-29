import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from lxml import etree
import requests
import csv
import pandas as pd


def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except:
        return False
    return True


def scroll_to_bottom(iteration=None):
    xpath_sidebar = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')
    if(iteration == None):
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", xpath_sidebar)
        time.sleep(2)
    else:
        for i in range(1, iteration):
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", xpath_sidebar)
            time.sleep(2)

def url_hit(data_latitude, data_longitude) :
    try : 
        data = []
        for latitude, longitude in zip (data_latitude, data_longitude) :
            start_time = time.time()
            try : 
                url = f'https://www.google.com/maps/search/Bulutangkis/@{latitude},{longitude},12.58z?entry=ttu' 
                print(f"Start in {url}")
                driver.get(url)
                
                time.sleep(2)
                
                try :
                    for i in range(1, 100):
                        # scroll down to bottom sidebar
                        scroll_to_bottom()
                        
                        # xpath_endsidebar = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[243]/div/p/span/span')
                        if(check_exists_by_xpath('/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[243]/div/p/span/span')):
                            scroll_to_bottom(2)
                            print("End scroll down !!")
                            try :
                                # Dapatkan HTML halaman web setelah di-render
                                html = driver.page_source
                                # Gunakan BeautifulSoup untuk mengekstrak data
                                soup = BeautifulSoup(html, 'lxml')
                                tes = soup.find_all('div', class_='bJzME tTVLSc')
                                #start crawling data !
                                for cari in tes:
                                    hrefs = cari.find_all('a', class_='hfpxzc')
                                    for href in hrefs:
                                        href_value = href.get('href')
                                        data.append({'URL': href_value} if href_value else {'URL': '-'})
                                        
                                    poi_names = cari.find_all('div', class_='qBF1Pd fontHeadlineSmall')
                                    for poi in poi_names:
                                        poinames_value = poi.text.strip() 
                                        data.append({'Name': poinames_value} if poinames_value else {'Name': '-'})

                                    ratings = cari.find_all('span', class_='MW4etd')
                                    for rating in ratings:
                                        ratings_value = rating.text.strip()
                                        data.append({'Rating': ratings_value} if ratings_value else {'Rating': '-'})
                                    
                                    address_schema = cari.find_all('div', class_='Nv2PK tH5CWc THOPZb')
                                    found_addresses = set()
                                    for address_testing in address_schema :                
                                        tagsaddress_elements = cari.find_all('div', class_='W4Efsd')
                                        for tagsaddress1 in tagsaddress_elements :
                                            tagsaddress1_value = tagsaddress1.find_all('div', class_='W4Efsd')
                                            for tagsaddress2 in tagsaddress1_value :
                                                tagsaddress2_value = tagsaddress2.findParents('div', class_='W4Efsd')
                                                for tagsaddress3 in tagsaddress2_value :
                                                    tagsaddress3_value = tagsaddress3.text.strip()
                                                    # Kondisi untuk memeriksa apakah alamat sudah ditemukan sebelumnya
                                                    if tagsaddress3_value not in found_addresses:
                                                        found_addresses.add(tagsaddress3_value)
                                                        data.append({'Address': tagsaddress3_value} if tagsaddress3_value else {'Address': '-'})

                            except Exception as e :
                                print("Terdapat error dibagian Crawling data(Function scrape_data)")
                            break
                
                except Exception as e :
                    print(f"Ada error ni di request {url} -> {e}")
                    
                print(f'url {url} sudah selesai load')              
    
            except TimeoutError :
                print(f'Teeett habis waktu jadi error di {url}')
                
            df = pd.DataFrame(data, columns=['URL','Name', 'Rating', 'Address'])
            df.head()
            print(data)
            df.to_csv(r'C:\Users\bputra\OneDrive - ESRI Indonesia\PT ESRI Indonesia\Research\code-script\17_scrapping_gmaps\gmaps\output\testing1_scrape_gmaps_bulutangkis',index=False, encoding='utf-8-sig',sep=';')
                
            end_time = time.time()
            
            execution_time = (end_time - start_time)/60
            print(f"Waktu yang dibutuhkan {execution_time:.2f} menit")
        
        print("Data sudah selesai di scrapping, horee !!!")
    
    except Exception as e :
        print('error nih haduhhh')

#data = r"D:\SCRIPT - ARCPY - PYTHON\script-python-working-in-esri\17_scrapping_gmaps\gmaps\input\kabkot_list_and_xy_sample.csv"
data = r"C:\Users\bputra\OneDrive - ESRI Indonesia\PT ESRI Indonesia\Research\code-script\17_scrapping_gmaps\gmaps\input\kabkot_list_and_xy_bulutangkis.csv"
df = pd.read_csv(data, delimiter=";")
pd.DataFrame(df)

data_lat = df['lat']
data_long = df['long']

driver = webdriver.Chrome()
url_hit(data_lat, data_long)
time.sleep(2)
driver.quit()