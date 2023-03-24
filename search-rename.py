import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# define the search string
search_string = "your_article_name"

# read the excel file
excel_file = pd.read_excel('path/to/excel_file.xlsx')

# create a list of article names from the excel file
article_names = excel_file['Article Name'].tolist()

# create a dictionary to store the downloaded and not downloaded files
downloaded_files = {}
not_downloaded_files = {}

# loop through the article names and search on sci-hub.ru
for article_name in article_names:
    # check if the article name contains the search string
    if search_string in article_name:
        # make a request to sci-hub.ru
        url = f"https://sci-hub.ru/{article_name}"
        response = requests.get(url)
        
        # check if the request was successful
        if response.status_code == 200:
            # parse the HTML response
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # find the link to the PDF file
            pdf_link = soup.find('iframe')['src']
            
            # download the PDF file
            pdf_response = requests.get(pdf_link)
            if pdf_response.status_code == 200:
                # save the PDF file with a new name
                pdf_filename = f"{search_string} - {article_name}.pdf"
                with open(pdf_filename, 'wb') as f:
                    f.write(pdf_response.content)
                
                # add the file to the downloaded files dictionary
                downloaded_files[article_name] = pdf_filename
            else:
                # add the file to the not downloaded files dictionary
                not_downloaded_files[article_name] = "Failed to download PDF"
        else:
            # add the file to the not downloaded files dictionary
            not_downloaded_files[article_name] = "Article not found on sci-hub.ru"

# create a new file with the downloaded and not downloaded files
with open(f"{search_string} - downloaded_files.txt", 'w') as f:
    f.write("Downloaded files:\n")
    for article_name, filename in downloaded_files.items():
        f.write(f"{article_name}: {filename}\n")
    f.write("\nNot downloaded files:\n")
    for article_name, error_message in not_downloaded_files.items():
        f.write(f"{article_name}: {error_message}\n")
