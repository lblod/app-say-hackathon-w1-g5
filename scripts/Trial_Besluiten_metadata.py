import os
import pandas as pd
import requests
import rdflib

# Read the CSV file
file_path = 'scripts/aanduidingsobjecten.csv'
df = pd.read_csv(file_path, delimiter=",", skiprows=5)

# Create 'besluiten' folder if it doesn't exist

output_folder = 'scripts/besluiten'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to fetch RDF data
def fetch_rdf_data(besluit_id):
    url = f"https://id.erfgoed.net/besluiten/{besluit_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Loop over the first 10 rows in the DataFrame
for index, row in df.iterrows():
    if index >= 10:
        break  # Stop after processing 10 rows
    besluiten_list = row['besluiten'].split(',')  # Assuming 'besluiten' is a comma-separated string
    
    # Loop over each 'besluit' in the list
    for besluit_id in besluiten_list:
        besluit_id = besluit_id.strip()  # Clean up any extra spaces
        rdf_data = fetch_rdf_data(besluit_id)
        
        if rdf_data:
            # Create a new RDF graph for each 'besluit'
            g = rdflib.Graph()
            g.parse(data=rdf_data, format="turtle")
            
            # Save each RDF data as a separate file in the 'besluiten' folder
            file_name = os.path.join(output_folder, f"besluit_{besluit_id}.ttl")
            g.serialize(destination=file_name, format="turtle")
            print(f"RDF data for {besluit_id} saved to {file_name}.")
        else:
            print(f"Failed to retrieve data for ID: {besluit_id}")

# #For reference the data to also get the pdf
# import requests

# url = "https://id.erfgoed.net/besluiten/14870/bestanden/28968"
# response = requests.get(url, allow_redirects=True)

# if response.status_code == 200:
#     with open("BesluitAG_20191112.pdf", 'wb') as f:
#         f.write(response.content)
#     print("Download successful!")
# else:
#     print(f"Failed to download file: {response.status_code}")

