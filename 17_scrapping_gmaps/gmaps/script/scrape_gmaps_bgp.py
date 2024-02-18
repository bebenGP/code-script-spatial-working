import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

data = r"D:\SCRIPT - ARCPY - PYTHON\script-python-working-in-esri\17_scrapping_gmaps\gmaps\input\kabkot_list_and_xy_sample.csv"
df = pd.read_csv(data, delimiter=";")
#pd.DataFrame(df)

data_lat = df['lat']
data_long = df['long']


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
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


def scrape_data():
    # Daftar XPath untuk setiap informasi
    xpath_urls = [
        '/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{}]/div/div[2]/div[4]/div[1]/div/div/div[2]/div[1]/div[2]',
        '/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{}]/div/div[2]/div[4]/div[1]/div/div/div[2]/div[3]/div/span[2]/span/span[1]',
        '/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{}]/div/div[2]/div[4]/div[1]/div/div/div[2]/div[4]/div[1]/span[1]/span',
        '/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{}]/div/div[2]/div[4]/div[1]/div/div/div[2]/div[4]/div[1]/span[2]/span[2]',
        '/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{}]/div/div[2]/div[4]/div[1]/div/div/div[2]/div[4]/div[2]/span[2]/span[2]'
    ]
    xpath_href = ['/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{}]/div/a']
    #xpath_href = ['//a[@class="hfpxzc"]']
    
    # List untuk menyimpan semua data
    all_data = []

    # Loop untuk mengekstrak informasi dari setiap elemen
    for i in range(3, 12, 2):  # misalnya, untuk nomor 3, 5, 7, 9, 11
        data = []
        for xpath in xpath_urls:
            xpath = xpath.format(i)
            #print(xpath)
            try :
                WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                element = driver.find_element(By.XPATH, xpath)
                information = element.text
                data.append(information)
            except NoSuchElementException:
                # Jika elemen tidak ditemukan, tambahkan string kosong ke dalam list
                data.append('')
                
        for xpath_xy in xpath_href:
            xpath_xy = xpath_xy.format(i)
            try:
                elements = driver.find_elements(By.XPATH, xpath_xy)
                for element_xy in elements:
                    information_href = element_xy.get_attribute('href')
                    #information_data = element.get_attribute('aria-label')
                    data.append(information_href)
            except NoSuchElementException:
                # Jika elemen tidak ditemukan, tambahkan string kosong ke dalam list
                data.append(('',''))
        
        all_data.append(data)
    try :    
        # Buat DataFrame dari list all_data
        df = pd.DataFrame(all_data, columns=['poi_name', 'ratings', 'tags', 'address', 'telp', 'url'])
        # Simpan DataFrame ke dalam file CSV
        df.to_csv('scraped_data_testing4.csv', sep=';', index=False)
    except Exception as e :
        print(f"Error bagian saving data to csv {e}")
        
    # Cetak semua data yang telah diambil
    for info in all_data:
        print(info)
            
def url_hit(data_latitude, data_longitude) :
    try : 
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
                            
                            break
                
                except Exception as e :
                    print(f"Ada error ni di request {url} -> {e}")
                    
                print(f'url {url} sudah selesai load')
                
                try :
                    #start crawling data !
                    scrape_data()
                except Exception as e :
                    print(f"Terdapat error dibagian Crawling data(Function scrape_data) -> {e}")
                
            except TimeoutError :
                print(f'Teeett habis waktu jadi error di {url}')
                
            end_time = time.time()
            
            execution_time = (end_time - start_time)/60
            print(f"Waktu yang dibutuhkan {execution_time:.2f} menit")

        print("Data sudah selesai di scrapping, horee !!!")
        
    except Exception as e :
        print('error nih haduhhh')

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

driver = webdriver.Chrome()
url_hit(data_lat, data_long)
time.sleep(2)
driver.quit()