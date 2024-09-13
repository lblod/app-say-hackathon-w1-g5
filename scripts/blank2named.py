# This script replaces blank nodes with named nodes
import sys
import itertools
from rdflib import Graph, Namespace
from rdflib.namespace import SKOS, DCTERMS, FOAF, XSD, RDF, RDFS
from rdflib.term import Node, URIRef, BNode, Literal
import uuid

MU = Namespace('http://mu.semte.ch/vocabularies/core/')
EX = Namespace('https://inventaris.onroerenderfgoed.be/')
AT = Namespace('https://id.erfgoed.net/thesauri/aanduidingstypes/')
BLANK = Namespace('https://example.org/')

def blank2named(node: Node, blanks: dict[BNode, Node] = {}, counter =
                itertools.count()):
    if isinstance(node, BNode):
        if node not in blanks:
            blanks[node] = BLANK[str(next(counter))]
        return blanks[node]

    return node

if __name__ == "__main__":

    if len(sys.argv) <= 2:
        print("Not enough arguments", file=sys.stderr)
        exit(1)

    g_src = Graph()
    g_src.parse(sys.argv[1])
    g = Graph()
    g.bind('ex', EX)
    g.bind('blank', BLANK)
    g.bind('mu', MU)
    g.bind('at', AT)

    for triple in g_src:
        s, p, o = tuple(blank2named(node) for node in triple)
        if p == RDF.type:
            random_uuid = str(uuid.uuid4())
            g.add((s, MU.uuid, Literal(random_uuid)))
        g.add((s, p, o))

    g.serialize(destination=sys.argv[2])
