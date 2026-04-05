from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def scrape_dynamic():
    driver = webdriver.Chrome()

    driver.get("http://quotes.toscrape.com/js/")
    time.sleep(100)

    quotes = driver.find_elements(By.CLASS_NAME, "quote")

    data = []

    for quote in quotes:
        text = quote.find_element(By.CLASS_NAME, "text").text
        author = quote.find_element(By.CLASS_NAME, "author").text

        data.append({
            "text": text,
            "author": author
        })

    driver.quit()
    return data