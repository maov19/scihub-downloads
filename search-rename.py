from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from itertools import zip_longest
import pandas as pd
import time
import os

# Read the Excel file with the article names
df = pd.read_excel(r'C:\Users\marti\OneDrive\Desktop\andrea\search-rename\article-list.xlsx')

# Create two empty lists to store the downloaded and not downloaded articles
downloaded_articles = []
not_downloaded_articles = []

# Initialize the webdriver (you'll need to specify the path to your own driver)
chromeOptions = Options()
# chromeOptions.headless = False
prefs = {"download.default_directory" : r"C:\Users\marti\OneDrive\Desktop\andrea\search-rename\downloaded_articles"}
chromeOptions.add_experimental_option("prefs", prefs)
service = Service(r'C:\Users\marti\OneDrive\Desktop\andrea\search-rename\chromedriver.exe')
browser = webdriver.Chrome(service=service, options=chromeOptions)


# download pdfs
for article_name in df['Article Name']:
    try:
        # Open the sci-hub website
        browser.get('https://sci-hub.ru/')
        # Wait for the page to load
        time.sleep(30)

        # Find the search bar and enter the article name
        search_bar = browser.find_element(by=By.NAME, value='request')
        search_bar.send_keys(article_name)
        search_bar.send_keys(Keys.RETURN)

        # Wait for the page to load
        time.sleep(10)

        # Check if the article was found
        save_button = browser.find_element(by=By.XPATH, value='/html/body/div[3]/div[1]/button')
        # if browser.find_elements_by_css_selector('#article'):
        # if save_button:
        # Find the "Save" button and click it
        save_button.click()

        # Wait for the download to finish
        time.sleep(10)

        # Rename the downloaded file to the article name
        old_file_name = 'sci-hub.pdf'
        new_file_name = article_name + '.pdf'
        os.rename(old_file_name, new_file_name)

        # Add the article to the downloaded list
        downloaded_articles.append(article_name)
        # else:
        #     # Add the article to the not downloaded list
        #     not_downloaded_articles.append(article_name)
    except:
        # If there was an error, add the article to the not downloaded list
        not_downloaded_articles.append(article_name)

# log downloaded and not downloaded pdfs
zipped = list(zip_longest(downloaded_articles, not_downloaded_articles, fillvalue=''))
result_df = pd.DataFrame(zipped, columns=['Downloaded Articles', 'Not Downloaded Articles'])
result_df.to_excel('result.xlsx', index=False)

# Close the browser
# browser.quit()
