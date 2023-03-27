from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from itertools import zip_longest
import pandas as pd
import time
import os

# location of folder for downloaded articles
downloads_folder = r"C:\Users\marti\OneDrive\Desktop\andrea\search-rename\downloaded_articles"

# location of excel file with the article names
excel_articles = r'C:\Users\marti\OneDrive\Desktop\andrea\search-rename\article-list.xlsx'
df = pd.read_excel(excel_articles)

# location of webdriver 
webdriver_location = r'C:\Users\marti\OneDrive\Desktop\andrea\search-rename\chromedriver.exe'

# Create two empty lists to store the downloaded and not downloaded articles
downloaded_articles = []
not_downloaded_articles = []

# Initialize the webdriver (you'll need to specify the path to your own driver)
chromeOptions = Options()
# chromeOptions.headless = False
prefs = {"download.default_directory" : downloads_folder}
chromeOptions.add_experimental_option("prefs", prefs)
service = Service(webdriver_location)
browser = webdriver.Chrome(service=service, options=chromeOptions)

# download pdfs
for idx, row in df.iterrows():
    try:
        article_id = row['id']
        article_name = row['Article Name']

        # Open the sci-hub website
        browser.get('https://sci-hub.se/')
        # Wait for the page to load, 40 secs for the 1st try
        if idx == 0:
            time.sleep(40)
        else:
            time.sleep(5)
        # Find the search bar and enter the article name
        search_bar = browser.find_element(by=By.NAME, value='request')
        search_bar.send_keys(article_name)
        search_bar.send_keys(Keys.RETURN)

        # Wait for the page to load, 40 secs for the 1st try
        if idx == 0:
            time.sleep(40)
        else:
            time.sleep(5)

        # click on download button
        save_button = browser.find_element(by=By.XPATH, value='/html/body/div[3]/div[1]/button')
        # if browser.find_elements_by_css_selector('#article'):
        # if save_button:
        # Find the "Save" button and click it
        save_button.click()

        # Wait for the download to finish
        time.sleep(5)

        # Rename the downloaded file to the article name
        # Step 1: Extract the desired name from the ID column
        desired_name = str(article_id) + '.pdf'

       # Step 2: Get the path of the most recently downloaded file
        files = os.listdir(downloads_folder)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(downloads_folder, x)), reverse=True)
        most_recent_file = files[0]
        most_recent_file_path = os.path.join(downloads_folder, most_recent_file)

        # Step 3: Rename the file with the desired name
        new_file_path = os.path.join(downloads_folder, desired_name)
        os.rename(most_recent_file_path, new_file_path)

        # Add the article to the downloaded list
        downloaded_articles.append(article_name)
    except:
        # If there was an error, add the article to the not downloaded list
        not_downloaded_articles.append(article_name)

# log downloaded and not downloaded pdfs
zipped = list(zip_longest(downloaded_articles, not_downloaded_articles, fillvalue=''))
result_df = pd.DataFrame(zipped, columns=['Downloaded Articles', 'Not Downloaded Articles'])
result_df.to_excel('result.xlsx', index=False)

# Close the browser
# browser.quit()
