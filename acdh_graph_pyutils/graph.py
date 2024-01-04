from typing import TypedDict
from rdflib import Graph, Literal, URIRef, RDF, RDFS, OWL, Namespace, plugin, ConjunctiveGraph
from rdflib.store import Store
from acdh_graph_pyutils.namespaces import NAMESPACES


Namespaces = TypedDict('Namespaces', {
    "key": Namespace,
})


def create_empty_graph(
    namespaces: Namespaces = NAMESPACES,
    identifier: URIRef = None,
    store: Store = None
) -> Graph:
    """
    Returns an empty graph with the namespaces defined in the namespaces.py file.
    """
    g = Graph(identifier=identifier, store=store)
    for key, value in namespaces.items():
        g.bind(key, value)
    return g


def create_custom_triple(
    subject: URIRef,
    predicate: Namespace,
    object: URIRef | Literal,
) -> Graph:
    """
    Returns a rdflib Graph object containing a custom rdflib triple object.
    """
    g = Graph()
    g.add((subject, predicate, object))
    return g


def create_type_triple(
    subject: URIRef,
    object: URIRef,
) -> Graph:
    """
    Returns a rdflib Graph object containing a RDF.type triple object.
    """
    g = Graph()
    g.add((subject, RDF.type, object))
    return g


def create_label_triple(
    subject: URIRef,
    object: Literal,
) -> Graph:
    """
    Returns a rdflib Graph object containing a RDF.label triple object.
    """
    g = Graph()
    g.add((subject, RDFS.label, object))
    return g


def create_value_triple(
    subject: URIRef,
    object: Literal,
) -> Graph:
    """
    Returns a rdflib Graph object containing a RDF.value triple object.
    """
    g = Graph()
    g.add((subject, RDF.value, object))
    return g


def create_sameAs_triple(
    subject: URIRef,
    object: URIRef,
) -> Graph:
    """
    Returns a rdflib Graph object containing a OWL.sameAs triple object.
    """
    g = Graph()
    g.add((subject, OWL.sameAs, object))
    return g


def serialize_graph(
    graph: Graph,
    format: str = "ttl",
    path: str = None,
) -> None:
    """
    Returns a serialized graph.
    """
    graph.serialize(path, format=format)


def create_memory_store(
    store: Store,
) -> Store:
    """
    Returns a memory store.
    """
    store = plugin.get("Memory", store)()
    return store


def create_conjunctive_graph(
    store: Store,
) -> ConjunctiveGraph:
    """
    Returns a conjunctive graph.
    """
    g = ConjunctiveGraph(store=store)
    return g
