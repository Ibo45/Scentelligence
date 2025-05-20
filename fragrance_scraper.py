import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

HEADERS = {'User-Agent': 'Mozilla/5.0'}

PERFUME_URLS = [
    "https://www.notino.de/dior/sauvage-eau-de-parfum-fuer-herren/",
    "https://www.notino.co.uk/dior/sauvage-eau-de-toilette-for-men/"
]

def scrape_notino(url):
    try:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')

        data = {
            "Name": "",
            "Brand": "",
            "Top Notes": "",
            "Heart Notes": "",
            "Base Notes": "",
            "Gender": "",
            "Scent Family": "",
            "URL": url
        }

        # Name
        try:
            data["Name"] = soup.select_one("h1").text.strip()
        except:
            pass

        # Brand (from breadcrumbs)
        try:
            brand_tag = soup.select_one("li.breadcrumb__item a span")
            if brand_tag:
                data["Brand"] = brand_tag.text.strip()
        except:
            pass

        # Notes
        note_section = soup.find("div", class_="pd-comp__composition")
        if note_section:
            notes = note_section.find_all("li")
            for n in notes:
                if "Top notes" in n.text:
                    data["Top Notes"] = n.text.replace("Top notes", "").strip(": ").strip()
                elif "Middle notes" in n.text:
                    data["Heart Notes"] = n.text.replace("Middle notes", "").strip(": ").strip()
                elif "Base notes" in n.text:
                    data["Base Notes"] = n.text.replace("Base notes", "").strip(": ").strip()

        # Gender
        if "for men" in url.lower():
            data["Gender"] = "Men"
        elif "for women" in url.lower():
            data["Gender"] = "Women"
        else:
            data["Gender"] = "Unisex"

        # Scent Family (guess from description)
        desc = soup.find("div", class_="pd-description__text")
        if desc:
            desc_text = desc.get_text().lower()
            for family in ["floral", "woody", "spicy", "oriental", "citrus", "fresh", "aquatic", "gourmand"]:
                if family in desc_text:
                    data["Scent Family"] = family
                    break

        return data

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return {}

def run_scraper():
    all_data = []
    for url in PERFUME_URLS:
        print(f"Scraping: {url}")
        info = scrape_notino(url)
        if not info or not info.get("Name"):
            print("⚠️ No data found.")
        else:
            print(f"→ {info.get('Name')} | {info.get('Brand')}")
            all_data.append(info)
            time.sleep(1)

    df = pd.DataFrame(all_data)
    df.to_csv("notino_fragrances.csv", index=False)
    print("✅ Data saved to notino_fragrances.csv")

if __name__ == "__main__":
    run_scraper()
