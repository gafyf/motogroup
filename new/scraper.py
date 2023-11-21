# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# import random
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from datetime import datetime
# import time

# # chrome_driver_path = "/usr/local/bin/chromedriver"/home/cloudshell-user/chromedriver-linux64/chromedriver

# # Set the path to Chromedriver
# # chrome_driver_path = "/home/cloudshell-user/chromedriver-linux64/chromedriver"

# # # Create ChromeOptions and set the path to Chromedriver
# # option = webdriver.ChromeOptions()
# # option.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")

# # service = Service(executable_path=chrome_driver_path)

# # option = Options()

# # option.add_argument("--disable-infobars")
# # option.add_argument("start-maximized")
# # option.add_argument("--disable-extensions")

# # option.add_argument('--headless')  # Optional: Run in headless mode without a visible browser window

# # option.add_argument("--disable-gpu")

# # # Pass the argument 1 to allow and 2 to block
# # option.add_experimental_option("prefs", { 
# #     "profile.default_content_setting_values.notifications": 2
# # })

# # driver = webdriver.Chrome(service=service, options=option)

# # Set the path to Chromedriver
# # chrome_driver_path = "/home/cloudshell-user/chromedriver-linux64/chromedriver"
# chrome_driver_path = "/usr/local/bin/chromedriver"

# # Create ChromeOptions and set the path to Chromedriver
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")

# # Configure other Chrome options
# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("start-maximized")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument('--headless')  # Optional: Run in headless mode without a visible browser window
# chrome_options.add_argument("--disable-gpu")

# # Pass the argument 1 to allow and 2 to block
# chrome_options.add_experimental_option("prefs", { 
#     "profile.default_content_setting_values.notifications": 2
# })

# # Initialize the Chrome webdriver with the specified options
# driver = webdriver.Chrome(options=chrome_options)


# driver.get('https://www.motociclismo.it/news')

# delay = random.randint(2, 7)

# actions = ActionChains(driver)

# time.sleep(delay)
# cookie_button = driver.find_element(By.XPATH,  '//*[@id="iubenda-cs-banner"]/div/div/div/div[3]/div[2]/button[1]')
# cookie_button.click()
# time.sleep(delay)
# time.sleep(delay)


# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# time.sleep(delay)
# driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
# time.sleep(delay)

# news_items = driver.find_elements(By.XPATH, '//*[@class="search-result"]')

# scraped_data = []

# # Loop through the news items
# for item in news_items:
#     time.sleep(delay)
#     pub_date = item.find_element(By.CSS_SELECTOR, '.block-content-date').text
#     # pub_date = item.find_element(By.XPATH, '//*[@class="block-content-date"]').text
#     time.sleep(delay)
#     formatted_pub_date = pub_date.strip()
#     print('Date date_text from site', pub_date)
#     current_date = datetime.now().strftime('%d %B %Y')
#     formatted_current_date = datetime.strptime(current_date, '%d %B %Y').strftime('%d %B %Y')
#     print('Date date_text today:', formatted_current_date)
#     if formatted_pub_date == formatted_current_date:
#         print('Date is today')
#         time.sleep(delay)
#         # item.click()
        
#         link_url = item.get_attribute("onclick")
#         url = link_url.split("'")[1]
#         time.sleep(delay)
#         driver.execute_script("window.open(arguments[0]);", url)

#         time.sleep(delay)
#         # Switch to the new tab
#         driver.switch_to.window(driver.window_handles[1])
        
#         time.sleep(delay)
#         time.sleep(delay)
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(delay)
#         article_title = driver.find_element(By.XPATH, '//*[@id="article-title"]').text
#         article_description = driver.find_element(By.XPATH, '//*[@class="description"]').text
#         print('article_description article_description', article_description)

#         # article_block_text = driver.find_element(By.XPATH, '//*[@class="articolo-block-text"]').text
#         block_text = driver.find_elements(By.CSS_SELECTOR, '.articolo-block-text')
#         for article_text in block_text:
#             article_block_text = article_text.text
#             print('article_block_text article_block_text', article_block_text)
#         article_images = driver.find_elements(By.CSS_SELECTOR, '.gallery-carousel-item')
#         article_image = article_images[0].find_element(By.XPATH, './/img').get_attribute('src')
#         print('article_image article_image', article_image)
#         driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
#         time.sleep(delay)
#         link = driver.current_url
#         print('Article_link', link)
#         print('Article_title', article_title)
#         print('Article_description', article_description)
#         print('Article_block_text', article_block_text)
#         print('Article_image', article_image)

#         time.sleep(delay)
#         time.sleep(delay)
#         scraped_data.append({'article_title': article_title, 'article_description': article_description, 'article_block_text': article_block_text, 'article_image': article_image, 'link': link})
#         print('scraped_data dupa append', scraped_data)
#         time.sleep(delay)
#         time.sleep(delay)
#         driver.close()
#         driver.switch_to.window(driver.window_handles[0])
#         time.sleep(delay)
#     else:
#         break

#     time.sleep(delay)

# # time.sleep(24 * 60 * 60)
# driver.quit()

