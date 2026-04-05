import requests
from bs4 import BeautifulSoup
import time
import random
def get_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)"
    ]
    return {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9"
    }

def fetch_page(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=get_headers(), timeout=10)

            if response.status_code == 200:
                return response.text
            else:
                print(f"[Retry {attempt+1}] Status Code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"[Retry {attempt+1}] Error: {e}")

        time.sleep(2)

    return None

def scrape_multiple_pages(pages=5):
    base_url = "http://quotes.toscrape.com/page/{}/"
    all_data = []

    for page in range(1, pages + 1):
        url = base_url.format(page)
        print(f"Scraping Page {page}...")

        html = fetch_page(url)

        if not html:
            print(f"Skipping page {page}")
            continue

        soup = BeautifulSoup(html, "lxml")
        quotes = soup.find_all("div", class_="quote")

        for quote in quotes:
            text_tag = quote.find("span", class_="text")
            author_tag = quote.find("small", class_="author")

            text = text_tag.get_text(strip=True) if text_tag else None
            author = author_tag.get_text(strip=True) if author_tag else None

            all_data.append({
                "text": text,
                "author": author
            })

        time.sleep(1)  

    return all_data

if __name__ == "__main__":
    data = scrape_multiple_pages(5)

    print(f"\nTotal Quotes Scraped: {len(data)}")
    print(data[:3])  # preview first 3