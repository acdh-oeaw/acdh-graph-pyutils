from rdflib import Namespace


NAMESPACES = {
    "cidoc": Namespace("http://www.cidoc-crm.org/cidoc-crm/"),
    "frbroo": Namespace("https://cidoc-crm.org/frbroo/sites/default/files/FRBR2.4-draft.rdfs#"),
    "int": Namespace("https://w3id.org/lso/intro/beta202304#"),
    "schema": Namespace("https://schema.org/"),
    "arche": Namespace("https://vocabs.acdh.oeaw.ac.at/schema#")
}

NSMAP = {
    "tei": "http://www.tei-c.org/ns/1.0",
    "xml": "http://www.w3.org/XML/1998/namespace",
}
