from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# шлях до chromedriver.exe
chromedriver_path = r"C:\Users\OS\Documents\chromedriver-win64"

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

url = "https://bookclub.ua/catalog/books/fantasy_books/koven-kniga-1"

driver.get(url)

# Очікуємо, поки кнопка з'явиться (максимум 10 секунд)
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "to_cart_button"))
    )
    buy_button = driver.find_element(By.CLASS_NAME, "to_cart_button")
    print("✅ Товар доступний для купівлі!")
except:
    print("❌ Немає в наявності.")

driver.quit()
