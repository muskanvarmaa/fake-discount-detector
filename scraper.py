import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import time

API_KEY = "8b3f967d2f9ee1a77a7fbe9fb9b22889"

products = [
    # Electronics - Amazon
    {"name": "boAt Rockerz 255 Z Plus", "category": "Electronics", "platform": "Amazon", "url": "https://www.amazon.in/dp/B0D6YS7PL7"},
    {"name": "Noise ColorFit Pro 4", "category": "Electronics", "platform": "Amazon", "url": "https://www.amazon.in/dp/B0BGSLP51D"},
    {"name": "Redmi Buds 4", "category": "Electronics", "platform": "Amazon", "url": "https://www.amazon.in/dp/B0C69PTC6M"},
    {"name": "Portronics Harmonics Z3", "category": "Electronics", "platform": "Amazon", "url": "https://www.amazon.in/dp/B0BJF85YRR"},
    {"name": "Boult Audio Z40 neckband", "category": "Electronics", "platform": "Amazon", "url": "https://www.amazon.in/dp/B0CHVTF8M7"},
    # Kitchen - Amazon
    {"name": "Milton Thermosteel Flask", "category": "Kitchen", "platform": "Amazon", "url": "https://www.amazon.in/dp/B0D45FF1HV"},
    {"name": "Prestige Electric Kettle 1.5L", "category": "Kitchen", "platform": "Amazon", "url": "https://www.amazon.in/dp/B01MQZ7J8K"},
    {"name": "Philips HL7756 Mixer Grinder", "category": "Kitchen", "platform": "Amazon", "url": "https://www.amazon.in/dp/B01GZSQJPA"},
    {"name": "Pigeon Induction Cooktop 1800W", "category": "Kitchen", "platform": "Amazon", "url": "https://www.amazon.in/dp/B01GFTEV5Y"},
    {"name": "Bajaj Majesty OTG 16L", "category": "Kitchen", "platform": "Amazon", "url": "https://www.amazon.in/dp/B0D2HYG2WJ"},
    {"name": "Havells Personal Blender", "category": "Kitchen", "platform": "Amazon", "url": "https://www.amazon.in/dp/B0FTZDLWRL"},
    # Beauty - Amazon
    {"name": "Mamaearth Vitamin C Facewash", "category": "Beauty", "platform": "Amazon", "url": "https://www.amazon.in/dp/B089W938BR"},
    {"name": "WOW Skin Science Onion Hair Oil", "category": "Beauty", "platform": "Amazon", "url": "https://www.amazon.in/dp/B08B2N5JNS"},
    {"name": "Plum Green Tea Face Scrub", "category": "Beauty", "platform": "Amazon", "url": "https://www.amazon.in/dp/B0C629LWVS"},
    {"name": "Himalaya Neem Face Pack", "category": "Beauty", "platform": "Amazon", "url": "https://www.amazon.in/dp/B005HBPEMQ"},
    {"name": "Biotique Honey Gel Face Cream", "category": "Beauty", "platform": "Amazon", "url": "https://www.amazon.in/dp/B00791D13Q"},
    # Books - Amazon
    {"name": "Atomic Habits", "category": "Books", "platform": "Amazon", "url": "https://www.amazon.in/dp/1847941834"},
    {"name": "Psychology of Money", "category": "Books", "platform": "Amazon", "url": "https://www.amazon.in/dp/9390166268"},
]

results = []

for i, product in enumerate(products):
    try:
        scraper_url = f"http://api.scraperapi.com?api_key={API_KEY}&url={product['url']}&country_code=in&render=true"
        
        print(f"[{i+1}/{len(products)}] Fetching {product['name']}...")
        response = requests.get(scraper_url, timeout=120)
        soup = BeautifulSoup(response.content, "html.parser")

        # Get current price
        price = None
        all_prices = soup.find_all("span", {"class": "a-price-whole"})
        if all_prices:
            price = all_prices[0].text.strip().replace(",", "").replace(".", "")

        # Get MRP
        mrp = None
        text_prices = soup.find_all("span", {"class": "a-text-price"})
        for tp in text_prices:
            offscreen = tp.find("span", {"class": "a-offscreen"})
            if offscreen:
                mrp = offscreen.text.strip().replace("₹", "").replace(",", "")
                break

        if not mrp:
            basis = soup.find("span", {"class": "basisPrice"})
            if basis:
                offscreen = basis.find("span", {"class": "a-offscreen"})
                if offscreen:
                    mrp = offscreen.text.strip().replace("₹", "").replace(",", "")

        price = price or "Not found"
        mrp = mrp or "Not found"

        print(f"   ✅ Price: ₹{price}, MRP: ₹{mrp}")

        results.append({
            "Date": date.today(),
            "Platform": product["platform"],
            "Product Name": product["name"],
            "Category": product["category"],
            "URL": product["url"],
            "MRP": mrp,
            "Current Price": price,
            "In Sale Period": "NO"
        })

        time.sleep(3)

    except Exception as e:
        print(f"   ❌ Error: {e}")
        results.append({
            "Date": date.today(),
            "Platform": product["platform"],
            "Product Name": product["name"],
            "Category": product["category"],
            "URL": product["url"],
            "MRP": "Error",
            "Current Price": "Error",
            "In Sale Period": "NO"
        })

try:
    existing = pd.read_excel("price_tracker.xlsx")
    df = pd.DataFrame(results)
    final = pd.concat([existing, df], ignore_index=True)
except FileNotFoundError:
    final = pd.DataFrame(results)

final.to_excel("price_tracker.xlsx", index=False)
print(f"\n✅ Done! {len(results)} products saved to price_tracker.xlsx!")