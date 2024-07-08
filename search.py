'''
import os
from bs4 import BeautifulSoup
import time

# Define the directory containing the HTML files
base_dir = "/Users/alfonsocalvanese/PyCharm Projects/ParserLeggi/RegionalLaws_2/"

# Variable to store the count of elements
total_count = 0

# Function to process each HTML file and count the elements
def count_elements_in_file(file_path):
    global total_count
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        elements = soup.find_all('span', class_='atto')
        total_count += len(elements)

# Iterate over the directories and files
for year in range(1951, 2025):

    for i in range(1, 53):
        file_name = f"{year}/laws_year_{i}.html"
        file_path = os.path.join(base_dir, file_name)
        if os.path.exists(file_path):
            count_elements_in_file(file_path)

time.sleep(0.1)

print(f"Total number of elements with class 'atto': {total_count}")
'''
'''
import pandas as pd

# Load the CSV file into a DataFrame
output_path = '/Users/alfonsocalvanese/PyCharm Projects/ParserLeggi/output_ps3.csv'
df = pd.read_csv(output_path)

# Convert 'Data Pubblicazione' to datetime format if it's not already
df['Data Pubblicazione'] = pd.to_datetime(df['Data Pubblicazione'], errors='coerce')

# Filter the DataFrame for rows where the year is 2013
laws_2013 = df[df['Data Pubblicazione'].dt.year == 2013]

# Count the number of rows (laws) for the year 2013
count_laws_2013 = laws_2013.shape[0]

print(f"Number of laws from the year 2013: {count_laws_2013}")

import pandas as pd

# Path to the CSV file
csv_path = '/Users/alfonsocalvanese/PyCharm Projects/ParserLeggi/output_ps3.csv'

# Load the CSV file into a DataFrame
df = pd.read_csv(csv_path)

# Check for duplicate rows
duplicates = df[df.duplicated()]

# Display the duplicate rows and their count
duplicate_count = duplicates.shape[0]
print(f"Number of duplicate rows: {duplicate_count}")
print(duplicates)

# Optionally, save the duplicates to a new CSV file
duplicates.to_csv('/Users/alfonsocalvanese/PyCharm Projects/ParserLeggi/duplicates.csv', index=False)
'''

import os
from bs4 import BeautifulSoup

# Directory containing the HTML files
directory_path = '/Users/alfonsocalvanese/PyCharm Projects/ParserLeggi/Leggi/1973'

# Text to search for
search_text = "Bilancio di Previsione della Regione per l' esercizio finanziario dell' anno 1973."

def search_text_in_html(file_path, search_text):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        if search_text in soup.get_text():
            print(f"Found '{search_text}' in {file_path}")

# Iterate over all files in the directory
for root, dirs, files in os.walk(directory_path):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            search_text_in_html(file_path, search_text)
