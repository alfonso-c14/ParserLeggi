import os
import time
from bs4 import BeautifulSoup
import pandas as pd

# Directory containing the HTML files
directory = "/Users/alfonsocalvanese/PyCharm Projects/ParserLeggi/RegionalLaws/"

# Initialize an empty list to store the data
data = []

# Iterate over the files in the directory
for year in range(1951, 2025):
    for file_number in range(1, 53):  # Assuming there can be up to 52 files per year
        file_path = os.path.join(directory, f"{year}/laws_year_{file_number}.html")
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                if html_content.strip():  # Check if file is not empty
                    # Parse HTML content using BeautifulSoup
                    soup = BeautifulSoup(html_content, 'html.parser')

                    # Extract data
                    results = soup.find_all('div', class_='singolo_risultato_collapse')
                    if not results:
                        print(f"No results found in file: {file_path}")
                    for result in results:
                        try:
                            regione = result.find('a').text.split('-')[0].strip()
                            stato = 'VIGENTE' if 'TESTO VIGENTE' in result.find('a').text else 'ABROGATO'
                            data_pubblicazione = result.find('a').text.split('Data pubblicazione: ')[-1].strip().replace(')', '')
                            titolo = result.find('span', class_='atto').text.strip()
                            try:
                                numero_legge = result.find('a').text.split(' n.')[1].split('del')[0].strip()
                            except IndexError:
                                numero_legge = 'N/A'
                            link = result.find('a')['href']

                            print(f"Extracted data: Regione={regione}, Numero Legge={numero_legge}, Titolo={titolo}, Stato={stato}, Data Pubblicazione={data_pubblicazione}, Link={link}")

                            data.append([regione, numero_legge, titolo, stato, data_pubblicazione, link])
                        except Exception as e:
                            print(f"Error processing result: {e}")
                            continue

            # Introduce a shorter delay to avoid processing too quickly
            time.sleep(0.1)

# Create DataFrame
df = pd.DataFrame(data, columns=['Regione', 'Numero Legge', 'Titolo', 'Stato', 'Data Pubblicazione', 'Link'])

# Convert 'Data Pubblicazione' to datetime format for proper sorting
df['Data Pubblicazione'] = pd.to_datetime(df['Data Pubblicazione'], format='%d/%m/%Y', errors='coerce')

# Drop rows with invalid 'Data Pubblicazione'
df = df.dropna(subset=['Data Pubblicazione'])

# Sort by 'Regione' alphabetically and 'Data Pubblicazione' chronologically
df = df.sort_values(by=['Regione', 'Data Pubblicazione'])

# Save to CSV
output_path = '/Users/alfonsocalvanese/PyCharm Projects/ParserLeggi/output.csv'
df.to_csv(output_path, index=False)

print(f"Data extracted and saved to {output_path}")
