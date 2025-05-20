from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# URLs to scrape


PERFUME_URLS = [
    "https://www.notino.de/creed/aventus-eau-de-parfum-fur-herren/",
    "https://www.notino.de/dior/sauvage-eau-de-toilette-fur-herren/"
]



def scrape_with_selenium(url, driver):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
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
        title_el = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        data["Name"] = title_el.text.strip()
    except:
        print("⚠️ Product name not found")

    # Brand from breadcrumbs
    try:
        brand_el = driver.find_element(By.CSS_SELECTOR, "li.breadcrumb__item a span")
        data["Brand"] = brand_el.text.strip()
    except:
        print("⚠️ Brand not found")

    # Composition table extraction
    try:
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        for row in rows:
            label = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.lower().strip()
            value = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text.strip()


            label = label.lower()

            if "kopf" in label or "top" in label:
                data["Top Notes"] = value
            elif "herz" in label or "middle" in label:
                data["Heart Notes"] = value
            elif "basis" in label or "base" in label:
                data["Base Notes"] = value
            elif "duftfamilien" in label or "fragrance category" in label:
                data["Scent Family"] = value

    except:
        print("⚠️ Notes or table not found")

    # Gender detection from URL
    if "for-men" in url:
        data["Gender"] = "Men"
    elif "for-women" in url:
        data["Gender"] = "Women"

    return data




def run_selenium_scraper():
    s = Service("chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode (no window)
    driver = webdriver.Chrome(service=s, options=options)

    all_data = []

    for url in PERFUME_URLS:
        print(f"Scraping: {url}")
        info = scrape_with_selenium(url, driver)
        print(f"→ {info.get('Name', '[no name]')} | {info.get('Brand', '[no brand]')}")
        all_data.append(info)

    driver.quit()
    df = pd.DataFrame(all_data)
    df.to_csv("notino_selenium_fragrances.csv", index=False)
    print("✅ Data saved to notino_selenium_fragrances.csv")

if __name__ == "__main__":
    run_selenium_scraper()
