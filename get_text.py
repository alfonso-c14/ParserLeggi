import os
import requests
from PyPDF2 import PdfReader
from io import BytesIO
import pandas as pd

# Load the CSV file
csv_path = '/Users/alfonsocalvanese/PyCharm Projects/ParserLeggi/new_output(noTrento).csv'
data = pd.read_csv(csv_path)

# Filter the data for the region 'Calabria'
calabria_data = data[data['Regione'].str.upper() == 'CALABRIA']

# Create the base directory for saving the text files
base_dir = 'calabria_laws'
os.makedirs(base_dir, exist_ok=True)

# Iterate through each row in the filtered dataframe
for index, row in calabria_data.iterrows():
    # Extract year from 'Data Pubblicazione'
    year = row['Data Pubblicazione'][:4]
    year_dir = os.path.join(base_dir, year)
    os.makedirs(year_dir, exist_ok=True)

    # Download the PDF
    pdf_url = row['Link']
    response = requests.get(pdf_url)

    if response.status_code == 200:
        # Open the PDF file in memory
        pdf_file = BytesIO(response.content)
        pdf_reader = PdfReader(pdf_file)

        # Extract text from each page
        extracted_text = ""
        for page in pdf_reader.pages:
            extracted_text += page.extract_text()

        # Save the extracted text to a file
        law_number = row['Numero Legge']
        file_name = f"legge_{law_number}.txt"
        file_path = os.path.join(year_dir, file_name)

        with open(file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(extracted_text)

        print(f"Processed law number {law_number} for year {year}.")
    else:
        print(f"Failed to download PDF for law number {law_number}.")

print("Processing completed.")
