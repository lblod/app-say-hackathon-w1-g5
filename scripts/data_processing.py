#Necessary libraries
import pandas as pd
import rdflib as rdf
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import SKOS, DCTERMS, FOAF, XSD, RDFS
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

# Function to check if a value is valid (not NaN or 'unknown')
def is_valid_value(value):
    if isinstance(value, float) and math.isnan(value):
        return False
    if value == "unknown" or value == "nan":
        return False
    return True

MU = Namespace('http://mu.semte.ch/vocabularies/core/')
EX = Namespace('https://inventaris.onroerenderfgoed.be/')

g = rdf.Graph()
g.bind('mu', MU)
g.bind('foaf', FOAF)
g.bind('dcterms', DCTERMS)
g.bind('rdfs', RDFS)
g.bind('xsd', XSD)

# Iterate over each row in the DataFrame and convert to Turtle
for index, row in df.iterrows():
    
    # Use the 'id' field directly for the URI (without slugifying it)
    uri = URIRef(f"{base_url}aanduidingsobjecten/{row['id']}")

    # Generate a random UUID for mu:uuid
    random_uuid = str(uuid.uuid4())
    
    # Ensure that 'naam' and other fields exist in the DataFrame
    naam = row.get('naam', 'unknown')  # Replace 'unknown' with a default value if 'naam' is missing

    g.add((uri, RDF.type, EX.Aanduidingsobject))
    g.add((uri, EX.type, Literal(row['type'])))
    g.add((uri, MU.uuid, Literal(random_uuid)))
    g.add((uri, DCTERMS.identifier, Literal(row['id'])))

    # Only write fields if they are valid (not NaN or "unknown")
    if is_valid_value(naam):
        g.add((uri, FOAF.name, Literal(naam)))
    if is_valid_value(row.get('locatie', 'unknown')):
        g.add((uri, DCTERMS.spatial, Literal(row['locatie'])))
    if is_valid_value(row.get('personen', 'unknown')):
        g.add((uri, FOAF.Person, Literal(row['personen'])))
    if is_valid_value(row.get('gebeurtenissen', 'unknown')):
        g.add((uri, DCTERMS.description, Literal(row['gebeurtenissen'])))
 
    for pred in ['provincie', 'gemeente', 'deelgemeente', 'nummers', 'stijl',
                 'typologie', 'context', 'materiaal', 'plantensoort',
                 'datering', 'gga_motivatie', 'themas']:
        if is_valid_value(row.get(pred, 'unknown')):
            g.add((uri, EX[pred], Literal(row[pred])))

    # Add dates with xsd:date datatype if valid
    issued_date = row.get('geldig vanaf', 'unknown')
    if is_valid_value(issued_date):
        g.add((uri, DCTERMS.issued, Literal(issued_date, datatype=XSD.date)))
    
    valid_date = row.get('geldig tot', 'unknown')
    if is_valid_value(valid_date):
        g.add((uri, DCTERMS.valid, Literal(valid_date, datatype=XSD.date)))
    
    if is_valid_value(row.get('geldigheid opmerkingen', 'unknown')):
        g.add((uri, RDFS.comment, Literal(row['geldigheid opmerkingen'])))
    if is_valid_value(row.get('besluiten', 'unknown')):
        g.add((uri, EX.besluiten_identifier, Literal(row['besluiten'])))

    if is_valid_value(row.get('dataverantwoordelijke', 'unknown')):
        g.add((uri, EX.dataverantwoordelijke, Literal(row['dataverantwoordelijke'])))
    if is_valid_value(row.get('toelatingsplichtige handelingen', 'unknown')):
        g.add((uri, EX.toelatingsplichtige_handelingen, Literal(row['toelatingsplichtige handelingen'])))

g.serialize(destination='scripts/aanduidingsobjecten.ttl')
