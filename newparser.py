import os
import time
import re
from bs4 import BeautifulSoup
import pandas as pd

# Directory containing the HTML files
directory = "/Users/alfonsocalvanese/PyCharm Projects/ParserLeggi/Leggi_html"

# Initialize an empty list to store the data
data = []

# Function to extract the region from the text
def extract_region(text):
    known_regions = [
        'ABRUZZO', 'BASILICATA', 'CALABRIA', 'CAMPANIA', 'EMILIA-ROMAGNA', 'FRIULI-VENEZIA-GIULIA',
        'LAZIO', 'LIGURIA', 'LOMBARDIA', 'MARCHE', 'MOLISE', 'PIEMONTE', 'PUGLIA', 'SARDEGNA', 'SICILIA',
        'TOSCANA', 'TRENTINO-ALTO ADIGE', 'UMBRIA', "VALLE D'AOSTA", 'VENETO', 'Trento (Prov.)'
    ]
    for region in known_regions:
        if region in text:
            return region
    return None

# Function to extract the year from the text
def extract_year(text):
    match = re.search(r'(\d{4})\s*-\s*TESTO', text)
    if match:
        return match.group(1)
    return None

# Iterate over the files in the directory
for year in range(1951, 2025):
    for month in range(1, 13):  # Iterate over months
        for file_number in range(1, 31):  # Assuming there can be up to 30 files per month
            file_path = os.path.join(directory, f"{year}/laws_year_{month}_{file_number}.html")
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
                                text = result.find('a').text
                                regione = extract_region(text)
                                if not regione:
                                    print(f"Unknown region in file: {file_path}")
                                    continue

                                stato = 'VIGENTE' if 'TESTO VIGENTE' in text else 'ABROGATO'
                                data_pubblicazione = re.search(r'Data pubblicazione:\s*(\d{2}/\d{2}/\d{4})', text)
                                if data_pubblicazione:
                                    data_pubblicazione = data_pubblicazione.group(1)
                                else:
                                    year_extracted = extract_year(text)
                                    data_pubblicazione = f'01/01/{year_extracted}' if year_extracted else 'N/A'

                                titolo = result.find('span', class_='atto').text.strip()
                                categoria = re.search(r'(?<=-)[\s\w]+(?=n.)', text)
                                categoria = categoria.group(0).strip() if categoria else 'N/A'
                                try:
                                    numero_legge = re.search(r'n.\s*(\d+)', text).group(1)
                                except AttributeError:
                                    numero_legge = 'N/A'
                                link = result.find('a')['href']

                                data.append([regione, numero_legge, titolo, categoria, stato, data_pubblicazione, link])
                            except Exception as e:
                                print(f"Error processing result: {e}")
                                continue

                # Introduce a shorter delay to avoid processing too quickly
                time.sleep(0.1)

# Create DataFrame
df = pd.DataFrame(data, columns=['Regione', 'Numero Legge', 'Titolo', 'Categoria', 'Stato', 'Data Pubblicazione', 'Link'])

# Convert 'Data Pubblicazione' to datetime format for proper sorting
df['Data Pubblicazione'] = pd.to_datetime(df['Data Pubblicazione'], format='%d/%m/%Y', errors='coerce')

# Drop rows with invalid 'Data Pubblicazione'
# df = df.dropna(subset=['Data Pubblicazione'])

# Remove duplicates
df = df.drop_duplicates()

# Sort by 'Regione' alphabetically and 'Data Pubblicazione' chronologically
df = df.sort_values(by=['Regione', 'Data Pubblicazione'])

# Save to CSV
output_path = '/Users/alfonsocalvanese/PyCharm Projects/ParserLeggi/output_def.csv'
df.to_csv(output_path, index=False)

print(f"Data extracted and saved to {output_path}")
