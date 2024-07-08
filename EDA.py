import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the CSV file
file_path = '/Users/alfonsocalvanese/PyCharm Projects/ParserLeggi/output_def3.csv'
data = pd.read_csv(file_path)

# Convert the publication date to datetime format and extract the year
data['Data Pubblicazione'] = pd.to_datetime(data['Data Pubblicazione'])
data['Year'] = data['Data Pubblicazione'].dt.year

# Number of laws per region per year
laws_per_region_year = data.groupby(['Regione', 'Year']).size().unstack(fill_value=0)

# Create the directory for saving plots if it doesn't exist
os.makedirs('graphs', exist_ok=True)

# Plotting the number of laws per region per year and saving the plots
for region in laws_per_region_year.index:
    plt.figure(figsize=(10, 6))
    plt.bar(laws_per_region_year.columns, laws_per_region_year.loc[region])
    plt.title(f'Number of Laws per Year in {region}')
    plt.xlabel('Year')
    plt.ylabel('Number of Laws')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'graphs/number_of_laws_per_year_{region}.png')
    plt.close()
