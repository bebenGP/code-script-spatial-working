from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

#driver = webdriver.Chrome()
#driver.maximize_window()
driver_tertutup = Options()
driver_tertutup.add_argument("--headless") #mode headless
driver = webdriver.Chrome(options=driver_tertutup)
driver.get('https://referensi.data.kemdikbud.go.id/pendidikan/paud')

#1
wait = WebDriverWait(driver, 5)
#driver.save_screenshot("home.png")
content = driver.page_source
#driver.quit()

#


    
