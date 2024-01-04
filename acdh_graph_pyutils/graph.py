from typing import TypedDict
from rdflib import Graph, Literal, URIRef, Namespace, plugin, ConjunctiveGraph
from rdflib.store import Store
from rdflib.namespace import OWL, RDF, RDFS
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
    graph: Graph,
    subject: URIRef,
    predicate: Namespace,
    object: URIRef | Literal,
) -> Graph:
    """
    Returns a rdflib Graph object containing a custom rdflib triple object.
    """
    graph.add((subject, predicate, object))
    return graph


def create_type_triple(
    graph: Graph,
    subject: URIRef,
    object: URIRef,
) -> Graph:
    """
    Returns a rdflib Graph object containing a RDF.type triple object.
    """
    graph.add((subject, RDF.type, object))
    return graph


def create_label_triple(
    graph: Graph,
    subject: URIRef,
    object: Literal,
) -> Graph:
    """
    Returns a rdflib Graph object containing a RDF.label triple object.
    """
    graph.add((subject, RDFS.label, object))
    return graph


def create_value_triple(
    graph: Graph,
    subject: URIRef,
    object: Literal,
) -> Graph:
    """
    Returns a rdflib Graph object containing a RDF.value triple object.
    """
    graph.add((subject, RDF.value, object))
    return graph


def create_sameAs_triple(
    graph: Graph,
    subject: URIRef,
    object: URIRef,
) -> Graph:
    """
    Returns a rdflib Graph object containing a OWL.sameAs triple object.
    """
    graph.add((subject, OWL.sameAs, object))
    return graph


def serialize_graph(
    graph: Graph,
    format: str = "ttl",
    to_file: str = "./graph.ttl",
) -> Graph:
    """
    Returns a serialized graph.
    """
    if isinstance(to_file, str):
        graph.serialize(format=format, destination=to_file)
    return graph.serialize(format=format)


def create_memory_store(
    store: Store = Store,
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
