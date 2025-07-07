import requests
from bs4 import BeautifulSoup
import time

URL = "https://bookclub.ua/catalog/books/fantasy_books/red-queen"
CHECK_INTERVAL = 10  # перевіряти кожні 10 секунд

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def check_product():
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Шукаємо кнопку "Купити"
    buy_button = soup.find("a", class_="to_cart_button")

    if buy_button:
        print("✅ Товар доступний! Ось лінк для додавання в кошик:")
        print("https://bookclub.ua" + buy_button["href"])
        return True
    else:
        print("❌ Немає в наявності...")
        return False

while True:
    if check_product():
        break
    time.sleep(CHECK_INTERVAL)
