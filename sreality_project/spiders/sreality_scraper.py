import psycopg2
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import csv

webdriver_path = 'C:/Users/jasar/Desktop/chroe_driver/chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)


def scrape_sreality(url, num_ads):
    ads_data = []
    for i in range(0, num_ads, 20):  # sreality.cz shows 20 ads per page
        page_url = f"{url}?strana={i // 20 + 1}"
        driver.get(page_url)

        time.sleep(2)  # wait for the page to load

        ads = driver.find_elements("css selector", '[property-list="estatesResource"] .property')
        print(ads)
        titles = [ad.text for ad in ads]

        print(titles)
        for ad in ads:
            title = ad.find_element("css selector", 'a.title').get_attribute('textContent').strip()

            time.sleep(1)  # add a delay before searching for the image element
            try:
                image_url = ad.find_element("css selector", 'a._2vc3VMce92XEJFrv8_jaeN img').get_attribute('src')
            except NoSuchElementException:
                image_url = "Image not found"
            ads_data.append([title, image_url])
            print(f"Scraped ad: {title}, {image_url}")  # Print the title and image URL of each ad after it's scraped.
            if len(ads_data) >= num_ads:
                break
        if len(ads_data) >= num_ads:
            break

    driver.quit()

    return ads_data


def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Image URL"])
        writer.writerows(data)

def save_to_postgres(csv_file, db_name, table_name):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(database=db_name, user='postgres', password="jasajernej", host='localhost', port='5436')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (title TEXT, image_url TEXT);"
    cursor.execute(create_table_query)

    # Read the data from the CSV file and insert into the table
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if it exists
        for row in reader:
            title = row[0]
            image_url = row[1]
            insert_query = f"INSERT INTO {table_name} (title, image_url) VALUES (%s, %s);"
            cursor.execute(insert_query, (title, image_url))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()



if __name__ == "__main__":
    url = "https://www.sreality.cz/en/search/for-sale/apartments"
    num_ads = 500
    ads_data = scrape_sreality(url, num_ads)
    write_to_csv(ads_data, '../../../sreality_ads.csv')

# Usage example
    csv_file = 'sreality_ads.csv'
    db_name = 'postgres'
    table_name = 'sreality_scraper_items'

    save_to_postgres(csv_file, db_name, table_name)
