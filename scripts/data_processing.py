#Necessary libraries
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import SKOS, DCTERMS, FOAF
import re
import uuid
import math

#collect the csv data
file_path = 'scripts/aanduidingsobjecten.csv'
df = pd.read_csv(file_path, delimiter=",",skiprows=5)

# Base URL for API requests
base_url = "https://inventaris.onroerenderfgoed.be/"

# Function to slugify fields like 'naam' or 'locatie', but not 'id'
def slugify(name):
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '-', name)
    return name.strip('-')

# Function to replace spaces with underscores for the 'type' field
def underscore_spaces(value):
    return value.replace(' ', '_')

# Function to check if a value is valid (not NaN or 'unknown')
def is_valid_value(value):
    if isinstance(value, float) and math.isnan(value):
        return False
    if value == "unknown" or value == "nan":
        return False
    return True

# Function to handle date literals and apply xsd:date type
def format_date(value):
    if is_valid_value(value):
        return f"\"{value}\"^^<http://www.w3.org/2001/XMLSchema#date>"
    return None

# Open output file for writing
with open('scripts/aanduidingsobjecten.ttl', 'w') as ttlfile:
    # Write prefixes at the top of the Turtle file
    ttlfile.write("@prefix mu: <http://mu.semte.ch/vocabularies/core/> .\n")
    ttlfile.write("@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n")
    ttlfile.write("@prefix dcterms: <http://purl.org/dc/terms/> .\n")
    ttlfile.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
    ttlfile.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n")
    ttlfile.write("@prefix ex: <https://inventaris.onroerenderfgoed.be/> .\n\n")

    # Iterate over each row in the DataFrame and convert to Turtle
    for index, row in df.iterrows():
        # Generate a random UUID for mu:uuid
        random_uuid = str(uuid.uuid4())
        
        # Use the 'id' field directly for the URI (without slugifying it)
        uri = f"<{base_url}aanduidingsobjecten/{row['id']}>"
        
        # Ensure that 'naam' and other fields exist in the DataFrame
        naam = row.get('naam', 'unknown')  # Replace 'unknown' with a default value if 'naam' is missing
        
        # Replace spaces with underscores in the 'type' field
        rdf_type = underscore_spaces(row['type'])
        
        # Write the RDF triples for this row
        ttlfile.write(f"{uri}\n")
        ttlfile.write(f"    a ex:{rdf_type};\n")  # 'type' field with underscores
        ttlfile.write(f"    mu:uuid \"{random_uuid}\";\n")
        ttlfile.write(f"    dcterms:identifier \"{row['id']}\";\n")
        
        # Only write fields if they are valid (not NaN or "unknown")
        if is_valid_value(naam):
            ttlfile.write(f"    foaf:name \"{naam}\";\n")
        if is_valid_value(row.get('locatie', 'unknown')):
            ttlfile.write(f"    dcterms:spatial \"{row['locatie']}\";\n")
        if is_valid_value(row.get('provincie', 'unknown')):
            ttlfile.write(f"    ex:provincie \"{row['provincie']}\";\n")
        if is_valid_value(row.get('gemeente', 'unknown')):
            ttlfile.write(f"    ex:gemeente \"{row['gemeente']}\";\n")
        if is_valid_value(row.get('deelgemeente', 'unknown')):
            ttlfile.write(f"    ex:deelgemeente \"{row['deelgemeente']}\";\n")
        if is_valid_value(row.get('nummers', 'unknown')):
            ttlfile.write(f"    ex:nummers \"{row['nummers']}\";\n")
        if is_valid_value(row.get('stijl', 'unknown')):
            ttlfile.write(f"    ex:stijl \"{row['stijl']}\";\n")
        if is_valid_value(row.get('typologie', 'unknown')):
            ttlfile.write(f"    ex:typologie \"{row['typologie']}\";\n")
        if is_valid_value(row.get('context', 'unknown')):
            ttlfile.write(f"    ex:context \"{row['context']}\";\n")
        if is_valid_value(row.get('materiaal', 'unknown')):
            ttlfile.write(f"    ex:materiaal \"{row['materiaal']}\";\n")
        if is_valid_value(row.get('plantensoort', 'unknown')):
            ttlfile.write(f"    ex:plantensoort \"{row['plantensoort']}\";\n")
        if is_valid_value(row.get('datering', 'unknown')):
            ttlfile.write(f"    ex:datering \"{row['datering']}\";\n")
        if is_valid_value(row.get('gga_motivatie', 'unknown')):
            ttlfile.write(f"    ex:gga_motivatie \"{row['gga_motivatie']}\";\n")
        if is_valid_value(row.get('personen', 'unknown')):
            ttlfile.write(f"    foaf:Person \"{row['personen']}\";\n")
        if is_valid_value(row.get('gebeurtenissen', 'unknown')):
            ttlfile.write(f"    dcterms:description \"{row['gebeurtenissen']}\";\n")
        if is_valid_value(row.get('themas', 'unknown')):
            ttlfile.write(f"    ex:themas \"{row['themas']}\";\n")
        
        # Add dates with xsd:date datatype if valid
        issued_date = format_date(row.get('geldig vanaf', 'unknown'))
        if issued_date:
            ttlfile.write(f"    dcterms:issued {issued_date};\n")
        
        valid_date = format_date(row.get('geldig tot', 'unknown'))
        if valid_date:
            ttlfile.write(f"    dcterms:valid {valid_date};\n")
        
        if is_valid_value(row.get('geldigheid opmerkingen', 'unknown')):
            ttlfile.write(f"    rdfs:comment \"{row['geldigheid opmerkingen']}\";\n")
        if is_valid_value(row.get('besluiten', 'unknown')):
            ttlfile.write(f"    ex:besluiten_identifier \"{row['besluiten']}\";\n")
        if is_valid_value(row.get('dataverantwoordelijke', 'unknown')):
            ttlfile.write(f"    ex:dataverantwoordelijke \"{row['dataverantwoordelijke']}\";\n")
        if is_valid_value(row.get('toelatingsplichtige handelingen', 'unknown')):
            ttlfile.write(f"    ex:toelatingsplichtige_handelingen \"{row['toelatingsplichtige handelingen']}\" .\n\n")
