# -----------------------------------------------------------------------------
# Google News Scraper using Selenium (Adapted for RUU Penyiaran)
# -----------------------------------------------------------------------------
# Description:
# This script uses the Selenium library to control a Chrome browser, scrape
# Google News search results for "RUU Penyiaran" over a specified date range,
# and save the results (title, description, link, source, date) to a CSV file.
# It scrapes data month-by-month to gather comprehensive results.

import pandas as pd
import time
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

# Set your research parameters here
# Using quotes for an exact match
KEYWORD = '"makan bergizi gratis"'
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 7, 1)
OUTPUT_FILENAME = 'mbg_news.csv'


def convert_relative_time_to_datetime(waktu_str):
    """
    Converts relative time strings (e.g., "5 jam yang lalu") from Indonesian
    to an absolute datetime object.
    """
    bulan_mapping = {
        'Jan': 'Jan', 'Feb': 'Feb', 'Mar': 'Mar', 'Apr': 'Apr', 'Mei': 'May', 'Jun': 'Jun',
        'Jul': 'Jul', 'Agu': 'Aug', 'Sep': 'Sep', 'Okt': 'Oct', 'Nov': 'Nov', 'Des': 'Dec'
    }

    waktu_str = waktu_str.lower()

    if 'jam yang lalu' in waktu_str:
        hours_ago = int(re.search(r'(\d+)', waktu_str).group(1))
        return datetime.now() - timedelta(hours=hours_ago)
    if 'hari yang lalu' in waktu_str or 'hari lalu' in waktu_str:
        days_ago = int(re.search(r'(\d+)', waktu_str).group(1))
        return datetime.now() - timedelta(days=days_ago)
    if 'minggu yang lalu' in waktu_str:
        weeks_ago = int(re.search(r'(\d+)', waktu_str).group(1))
        return datetime.now() - timedelta(weeks=weeks_ago)

    # Handle absolute dates like "20 Jun 2024"
    for id_bulan, en_bulan in bulan_mapping.items():
        if id_bulan.lower() in waktu_str:
            waktu_str = waktu_str.replace(id_bulan.lower(), en_bulan)
            try:
                # Attempt to parse format like "20 Jun 2024"
                return datetime.strptime(waktu_str, '%d %b %Y')
            except ValueError:
                continue
    return None  # Return None if no format matches


def main():
    """
    Main function to initialize the scraper and run the process.
    """
    print("Initializing Selenium WebDriver...")

    # --- 2. SETUP SELENIUM WEBDRIVER ---
    # This setup uses webdriver-manager to automatically handle the chromedriver,
    # making it much easier to run on different machines.
    options = Options()
    options.add_argument("--headless")  # Run Chrome in the background
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    all_articles_data = []

    # --- 3. LOOP THROUGH EACH MONTH ---
    current_date = START_DATE
    while current_date < END_DATE:
        start_of_month = current_date
        end_of_month = current_date + \
            relativedelta(months=1) - relativedelta(days=1)

        # Format dates for Google's URL parameter (MM/DD/YYYY)
        date_min = start_of_month.strftime('%m/%d/%Y')
        date_max = end_of_month.strftime('%m/%d/%Y')

        print(f"\n--- Scraping for period: {date_min} to {date_max} ---")

        # Construct the search URL
        formatted_keyword = KEYWORD.replace('"', '').replace(" ", "+")
        url = f"https://www.google.com/search?q={formatted_keyword}&tbs=cdr:1,cd_min:{date_min},cd_max:{date_max},sbd:1&tbm=nws"

        driver.get(url)
        time.sleep(2)  # Allow time for the page to load

        # --- 4. PAGINATION LOOP ---
        page_num = 1
        while True:
            print(f"Scraping page {page_num} for the current month...")
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # NOTE: Google can change these class names. If the script finds no articles,
            # this is the first place to check by inspecting the Google News page.
            news_elements = soup.find_all('div', class_='SoaBEf')

            if not news_elements:
                print("No more articles found on this page.")
                break

            for article in news_elements:
                try:
                    title = article.find('div', class_='n0jPhd').text.strip()
                    link = article.find('a', class_='WlydOe')['href']
                    source = article.find('span').text.strip()
                    description = article.find(
                        'div', class_='GI74Re').text.strip()
                    date_str = article.find(
                        'div', class_='OSrXXb').text.strip()

                    all_articles_data.append({
                        'title': title,
                        'description': description,
                        'link': link,
                        'source': source,
                        'date_string': date_str
                    })
                except Exception as e:
                    print(
                        f"   - Could not parse an article, skipping. Error: {e}")

            # Try to find and click the 'Next' button
            try:
                next_button = driver.find_element(By.ID, "pnnext")
                next_button.click()
                page_num += 1
                time.sleep(3)  # Wait for next page to load
            except NoSuchElementException:
                print(
                    "No 'Next' button found. Reached the end of results for this month.")
                break  # Exit the pagination loop

        # Move to the next month
        current_date += relativedelta(months=1)

    driver.quit()
    print("\n--- Scraping process complete. Now processing data. ---")

    # --- 5. PROCESS AND SAVE DATA ---
    if not all_articles_data:
        print("No articles were found in the specified date range.")
        return

    df = pd.DataFrame(all_articles_data)

    # Clean the data
    print("Deduplicating articles...")
    df.drop_duplicates(subset=['link'], inplace=True, keep='first')

    print("Converting dates...")
    df['published_date'] = df['date_string'].apply(
        convert_relative_time_to_datetime)

    # Sort and reorder columns
    df = df.sort_values(by='published_date', ascending=False)
    df = df[['published_date', 'title', 'source',
             'description', 'link', 'date_string']]

    print(f"\nSuccessfully collected {len(df)} unique articles.")
    print("--- Data Preview ---")
    print(df.head())

    # Save to CSV
    df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
    print(f"\nData successfully saved to '{OUTPUT_FILENAME}'")


if __name__ == "__main__":
    main()
