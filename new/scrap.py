# import json
import os
import boto3
import zipfile
import random
import time
# import schedule
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service



# Define the local directory to extract the contents
extraction_path = '/tmp/'

def chrome_path():
    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Define the S3 bucket and ZIP file name
    bucket_name = 'chrome-chromedriver'
    zip_file_key = 'https://chrome-chromedriver.s3.eu-central-1.amazonaws.com/chrome-chromedriver.zip'


    # Fetch the ZIP file from S3
    s3.download_file(bucket_name, zip_file_key, f'{extraction_path}chrome-chromedriver.zip')

    # Extract the contents of the ZIP file
    with zipfile.ZipFile(f'{extraction_path}chrome-chromedriver.zip', 'r') as zip_ref:
        zip_ref.extractall(extraction_path)

    # Add the extraction path to the system PATH so your Lambda function can find Chrome and ChromeDriver
    os.environ['PATH'] = f"{os.environ['PATH']}:{extraction_path}"

scraped_data = []

def scrape_data():

    chrome_driver_path = f"{extraction_path}chromedriver_linux64/chromedriver"

    # Create ChromeOptions and set the path to Chromedriver
    option = webdriver.ChromeOptions()
    option.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")

    service = Service(executable_path=chrome_driver_path)

    option = Options()

    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    option.add_argument('--headless')  # Optional: Run in headless mode without a visible browser window

    option.add_argument("--disable-gpu")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 2
    })

    driver = webdriver.Chrome(service=service, options=option)


    driver.get('https://www.motociclismo.it/news')

    delay = random.randint(2, 7)

    time.sleep(delay)
    cookie_button = driver.find_element(By.XPATH,  '//*[@id="iubenda-cs-banner"]/div/div/div/div[3]/div[2]/button[1]')
    cookie_button.click()
    time.sleep(delay)
    time.sleep(delay)


    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(delay)
    driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
    # time.sleep(delay)

    news_items = driver.find_elements(By.XPATH, '//*[@class="search-result"]')

    # scraped_data = []

    for item in news_items:
        # time.sleep(delay)
        pub_date = item.find_element(By.CSS_SELECTOR, '.block-content-date').text
        # time.sleep(delay)
        formatted_pub_date = pub_date.strip()
        print('Date date_text from site', pub_date)
        current_date = datetime.now().strftime('%d %B %Y')
        formatted_current_date = datetime.strptime(current_date, '%d %B %Y').strftime('%d %B %Y')
        print('Date date_text today:', formatted_current_date)
        if formatted_pub_date == formatted_current_date:
            print('Date is today')
            # time.sleep(delay)
            link_url = item.get_attribute("onclick")
            url = link_url.split("'")[1]
            # time.sleep(delay)
            driver.execute_script("window.open(arguments[0]);", url)

            time.sleep(delay)
            # Switch to the new tab
            driver.switch_to.window(driver.window_handles[1])
            
            time.sleep(delay)
            time.sleep(delay)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(delay)
            article_title = driver.find_element(By.XPATH, '//*[@id="article-title"]').text
            article_description = driver.find_element(By.XPATH, '//*[@class="description"]').text
            print('article_description article_description', article_description)

            block_text = driver.find_elements(By.CSS_SELECTOR, '.articolo-block-text')
            for article_text in block_text:
                article_block_text = article_text.text
                print('article_block_text article_block_text', article_block_text)
            article_images = driver.find_elements(By.CSS_SELECTOR, '.gallery-carousel-item')
            article_image = article_images[0].find_element(By.XPATH, './/img').get_attribute('src')
            print('article_image article_image', article_image)
            driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
            time.sleep(delay)
            link = driver.current_url
            print('Article_link', link)
            print('Article_title', article_title)
            print('Article_description', article_description)
            print('Article_block_text', article_block_text)
            print('Article_image', article_image)

            # time.sleep(delay)
            time.sleep(delay)
            scraped_data.append({'article_title': article_title, 'article_description': article_description, 'article_block_text': article_block_text, 'article_image': article_image, 'link': link})
            print('scraped_data dupa append', scraped_data)
            # time.sleep(delay)
            # time.sleep(delay)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(delay)
        else:
            break

        # time.sleep(delay)

    driver.close()
    driver.quit()
    
