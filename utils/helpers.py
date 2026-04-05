import random
import requests
import time

# -------- USER AGENTS --------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/118.0.0.0 Safari/537.36"
]

def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }


# -------- PROXIES --------
PROXIES = [
    "http://123.45.67.89:8080",
    "http://98.76.54.32:8000"
]

def get_proxy():
    proxy = random.choice(PROXIES)
    return {
        "http": proxy,
        "https": proxy  # same proxy for both
    }


# -------- REQUEST FUNCTION WITH RETRY --------
def fetch_url(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(
                url,
                headers=get_headers(),
                proxies=get_proxy(),
                timeout=10
            )

            if response.status_code == 200:
                return response.text

            print(f"[Retry {attempt+1}] Status: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"[Retry {attempt+1}] Error: {e}")

        time.sleep(2)

    return None


# -------- USAGE --------
if __name__ == "__main__":
    url = "http://quotes.toscrape.com"
    html = fetch_url(url)

    if html:
        print("Page fetched successfully!")
    else:
        print("Failed to fetch page.")