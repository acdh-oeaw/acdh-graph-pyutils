import unittest
import lxml.etree as ET

from lxml.etree import Element
from rdflib import Graph, Literal, URIRef, Namespace, plugin, ConjunctiveGraph
from rdflib.namespace import OWL, RDF, RDFS
from acdh_graph_pyutils.namespaces import NAMESPACES
from acdh_graph_pyutils.graph import (
    create_empty_graph,
    create_custom_triple,
    create_type_triple,
    create_label_triple,
    create_value_triple,
    create_sameAs_triple,
    serialize_graph,
    create_conjunctive_graph,
    create_memory_store
)
from acdh_graph_pyutils.string_utils import normalize_string, date_to_literal

sample = """
<TEI xmlns="http://www.tei-c.org/ns/1.0">
    <person xml:id="DWpers0091" sortKey="Gulbransson_Olaf_Leonhard">
        <persName xml:lang="fr">
            <forename>Olaf</forename>
            <forename type="unused" xml:lang="bg">Leonhard</forename>
            <surname>Gulbransson</surname>
        </persName>
        <birth when="1873-05-26">26. 5. 1873<placeName key="#DWplace00139"
                >Christiania (Oslo)</placeName></birth>
        <death>
            <date notBefore-iso="1905-07-04" when="1955" to="2000">04.07.1905</date>
            <settlement key="pmb50">
                <placeName type="pref">Wien</placeName>
                <location><geo>48.2066 16.37341</geo></location>
            </settlement>
        </death>
        <persName type="pref">Gulbransson, Olaf</persName>
        <persName type="full">Gulbransson, Olaf Leonhard</persName>
        <occupation type="prim" n="01">Zeichner und Maler</occupation>
        <occupation notBefore="1902" notAfter="1944" n="02">Mitarbeiter des <title
                level="j">Simplicissimus</title></occupation>
        <idno type="GND">118543539</idno>
    </person>
    <place xml:id="DWplace00092">
        <placeName type="orig_name">Reval (Tallinn)</placeName>
        <placeName xml:lang="de" type="simple_name">Reval</placeName>
        <placeName xml:lang="und" type="alt_label">Tallinn</placeName>
        <idno type="pmb">https://pmb.acdh.oeaw.ac.at/entity/42085/</idno>
        <idno type="URI" subtype="geonames">https://www.geonames.org/588409</idno>
        <idno subtype="foobarid">12345</idno>
        <location><geo>123 456</geo></location>
    </place>
    <place xml:id="DWplace00010">
        <placeName xml:lang="de" type="orig_name">Jaworzno</placeName>
        <idno type="pmb">https://pmb.acdh.oeaw.ac.at/entity/94280/</idno>
        <location><geo>123 456 789</geo></location>
    </place>
    <org xml:id="DWorg00001">
        <orgName xml:lang="de" type="orig_name">Stahlhelm</orgName>
        <orgName xml:lang="de" type="short">Stahlhelm</orgName>
        <orgName xml:lang="de" type="full">Stahlhelm, Bund der Frontsoldaten</orgName>
        <idno type="pmb">https://pmb.acdh.oeaw.ac.at/entity/135089/</idno>
        <idno type="gnd">https://d-nb.info/gnd/63616-2</idno>
    </org>
    <org xml:id="DWorg00002">
        <orgName xml:lang="de" type="orig_name">GDVP</orgName>
        <orgName xml:lang="de" type="short">GDVP</orgName>
        <orgName xml:lang="de" type="full">Großdeutsche Volkspartei</orgName>
        <idno type="pmb">https://pmb.acdh.oeaw.ac.at/entity/135090/</idno>
        <idno type="gnd">https://d-nb.info/gnd/410560-6</idno>
    </org>
    <place xml:id="DWplace00013">
        <placeName type="orig_name">Radebeul (?)</placeName>
        <placeName xml:lang="de">Radebeul</placeName>
        <placeName xml:lang="und" type="alt_label"></placeName>
        <idno type="pmb">https://pmb.acdh.oeaw.ac.at/entity/45569/</idno>
    </place>
    <bibl xml:id="DWbible01113">
        <title>Hansi4ever</title>
    </bibl>
    <person xml:id="hansi12343">
        <test></test>
    </person>
    <person xml:id="onlypersnameelement">
        <persName>Ronja, Hanna</persName>
    </person>
    <person xml:id="maxicosi">
        <persName><forename>maxi</forename><surname>cosi</surname></persName>
    </person>
</TEI>
"""


class TestTestTest(unittest.TestCase):
    """Tests for `acdh_graph_pyutils` package."""

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_001_create_memory_store(self):
        store = create_memory_store()
        self.assertIsNotNone(store)

    def test_002_create_empty_graph(self):
        g = create_empty_graph(
            namespaces=NAMESPACES,
            identifier=URIRef("http://example.com/identifier"),
            store=create_memory_store()
        )
        self.assertIsInstance(g, Graph)

    def test_003_serialize_graph(self):
        g = create_custom_triple(
            graph=create_empty_graph(
                namespaces=NAMESPACES,
                identifier=URIRef("http://example.com/identifier"),
                store=create_memory_store()
            ),
            subject=URIRef("http://example.com/subject"),
            predicate=OWL.sameAs,
            object=URIRef("http://example.com/object")
        )
        data = serialize_graph(graph=g, format="turtle", to_file="003.ttl")
        self.assertIn("http://example.com/subject", data)
        self.assertIn("http://example.com/object", data)
        self.assertIn("owl:sameAs", data)

    def test_004_create_custom_triple(self):
        g = create_custom_triple(
            graph=create_empty_graph(
                namespaces=NAMESPACES,
                identifier=URIRef("http://example.com/identifier"),
                store=create_memory_store()
            ),
            subject=URIRef("http://example.com/subject"),
            predicate=RDF.type,
            object=URIRef("http://example.com/object")
        )
        self.assertIsInstance(g, Graph)
        data = serialize_graph(graph=g, format="turtle", to_file="004.ttl")
        self.assertIn("http://example.com/subject", data)
        self.assertIn("http://example.com/object", data)
        self.assertIn("a <http:", data)

    def test_005_create_type_triple(self):
        g = create_type_triple(
            graph=create_empty_graph(
                namespaces=NAMESPACES,
                identifier=URIRef("http://example.com/identifier"),
                store=create_memory_store()
            ),
            subject=URIRef("http://example.com/subject"),
            object=URIRef("http://example.com/object")
        )
        self.assertIsInstance(g, Graph)
        data = serialize_graph(graph=g, format="turtle", to_file="005.ttl")
        self.assertIn("http://example.com/subject", data)
        self.assertIn("http://example.com/object", data)
        self.assertIn("a <http:", data)

    def test_006_create_value_triple(self):
        g = create_value_triple(
            graph=create_empty_graph(
                namespaces=NAMESPACES,
                identifier=URIRef("http://example.com/identifier"),
                store=create_memory_store()
            ),
            subject=URIRef("http://example.com/subject"),
            object=URIRef("http://example.com/object")
        )
        self.assertIsInstance(g, Graph)
        data = serialize_graph(graph=g, format="turtle", to_file="006.ttl")
        self.assertIn("http://example.com/subject", data)
        self.assertIn("http://example.com/object", data)
        self.assertIn("rdf:value", data)

    def test_007_create_label_triple(self):
        g = create_label_triple(
            graph=create_empty_graph(
                namespaces=NAMESPACES,
                identifier=URIRef("http://example.com/identifier"),
                store=create_memory_store()
            ),
            subject=URIRef("http://example.com/subject"),
            object=URIRef("http://example.com/object")
        )
        self.assertIsInstance(g, Graph)
        data = serialize_graph(graph=g, format="turtle", to_file="007.ttl")
        self.assertIn("http://example.com/subject", data)
        self.assertIn("http://example.com/object", data)
        self.assertIn("rdfs:label", data)

    def test_008_create_sameAs_triple(self):
        g = create_sameAs_triple(
            graph=create_empty_graph(
                namespaces=NAMESPACES,
                identifier=URIRef("http://example.com/identifier"),
                store=create_memory_store()
            ),
            subject=URIRef("http://example.com/subject"),
            object=URIRef("http://example.com/object")
        )
        self.assertIsInstance(g, Graph)
        data = serialize_graph(graph=g, format="turtle", to_file="008.ttl")
        self.assertIn("http://example.com/subject", data)
        self.assertIn("http://example.com/object", data)
        self.assertIn("owl:sameAs", data)

    def test_009_create_conjunctive_graph(self):
        store = create_memory_store()
        graph = create_empty_graph(
            namespaces=NAMESPACES,
            identifier=URIRef("http://example.com/identifier"),
            store=store
        )
        create_sameAs_triple(
            graph=graph,
            subject=URIRef("http://example.com/subject"),
            object=URIRef("http://example.com/object")
        )
        g = create_conjunctive_graph(
            store=store
        )
        self.assertIsInstance(g, Graph)
        data = serialize_graph(graph=g, format="trig", to_file="009.trig")
        self.assertIn("ns1:identifier", data)

    def test_010_normalize_string(self):
        string = "  This is a    test   string.  "
        self.assertEqual(normalize_string(string), "This is a test string.")

    def test_011_date_to_literal(self):
        date = "2000-01-01"
        self.assertEqual(date_to_literal(date), Literal("2000-01-01",
                                                        datatype=URIRef("http://www.w3.org/2001/XMLSchema#date")))
        date = "2000-01"
        self.assertEqual(date_to_literal(date), Literal("2000-01",
                                                        datatype=URIRef("http://www.w3.org/2001/XMLSchema#gYearMonth")))
        date = "2000"
        self.assertEqual(date_to_literal(date), Literal("2000",
                                                        datatype=URIRef("http://www.w3.org/2001/XMLSchema#gYear")))
        date = "2000-01-01T00:00:00"
        self.assertEqual(date_to_literal(date), Literal("2000-01-01T00:00:00",
                                                        datatype=URIRef("http://www.w3.org/2001/XMLSchema#dateTime")))
        date = "2000-01-01T00:00:00Z"
        self.assertEqual(date_to_literal(date), Literal("2000-01-01T00:00:00Z",
                                                        datatype=URIRef("http://www.w3.org/2001/XMLSchema#dateTime")))
        date = "2000-01-01T00:00:00+01:00"
        self.assertEqual(date_to_literal(date), Literal("2000-01-01T00:00:00+01:00",
                                                        datatype=URIRef("http://www.w3.org/2001/XMLSchema#dateTime")))
        date = "Before Christ"
        self.assertEqual(date_to_literal(date), Literal("Before Christ",
                                                        datatype=URIRef("http://www.w3.org/2001/XMLSchema#string")))
        date = ""
        self.assertEqual(date_to_literal(date), Literal("undefined", lang="en"))
        date = None
        self.assertEqual(date_to_literal(date), Literal("undefined", lang="en"))
