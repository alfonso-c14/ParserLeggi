from bs4 import BeautifulSoup
import pandas as pd
import os
import csv
import re
'''

import os
import pandas as pd
from bs4 import BeautifulSoup

# Directory dei file HTML
base_dir = '/Users/alfonsocalvanese/PyCharm Projects/ParserLeggi/RegionalLaws/'

# Lista per raccogliere i dati
data = []


# Funzione per estrarre dati da un file HTML
def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        print(f"Parsing file: {file_path}")  # Log del file corrente

        # Estrarre la tabella specifica
        table = soup.find('table', {'class': 'standard'})
        if not table:
            print(f"No table found in file: {file_path}")  # Log quando la tabella non è trovata
            return

        rows = table.find_all('tr')
        if not rows:
            print(f"No rows found in table for file: {file_path}")  # Log quando non ci sono righe nella tabella
            return

        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 6:
                print(f"Unexpected row format in file: {file_path}")  # Log per formato di riga inaspettato
                continue

            regione = cols[0].text.strip()
            numero_legge = cols[1].text.strip()
            titolo = cols[2].text.strip()
            stato = cols[3].text.strip()
            data_pubblicazione = cols[4].text.strip()
            link = cols[5].find('a')['href'].strip()

            data.append({
                'Regione': regione,
                'Numero Legge': numero_legge,
                'Titolo': titolo,
                'Stato': stato,
                'Data Pubblicazione': data_pubblicazione,
                'Link': link
            })


# Iterare sui file HTML
for subdir, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(subdir, file)
            parse_html(file_path)

# Creare un DataFrame con i dati estratti
df = pd.DataFrame(data)

# Mostrare i dati estratti
import ace_tools as tools;

tools.display_dataframe_to_user(name="Dati Estratti", dataframe=df)
'''

import os
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
                            data_pubblicazione = result.find('a').text.split('Data pubblicazione: ')[
                                -1].strip().replace(')', '')
                            titolo = result.find('span', class_='atto').text.strip()
                            try:
                                numero_legge = result.find('a').text.split(' n.')[1].split('del')[
                                    0].strip()
                            except IndexError:
                                numero_legge = 'N/A'
                            link = result.find('a')['href']

                            print(
                                f"Extracted data: Regione={regione}, Numero Legge={numero_legge}, Titolo={titolo}, Stato={stato}, Data Pubblicazione={data_pubblicazione}, Link={link}")

                            data.append([regione, numero_legge, titolo, stato, data_pubblicazione, link])
                        except Exception as e:
                            print(f"Error processing result: {e}")
                            continue

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
