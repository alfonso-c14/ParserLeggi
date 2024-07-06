import os
from bs4 import BeautifulSoup
import time

# Define the directory containing the HTML files
base_dir = "/Users/alfonsocalvanese/PyCharm Projects/ParserLeggi/RegionalLaws/"

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