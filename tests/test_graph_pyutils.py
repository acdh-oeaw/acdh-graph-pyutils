import unittest
import lxml.etree as ET

from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import OWL, RDF
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
from acdh_graph_pyutils.xml import (
    extract_begin_end,
    parse_xml,
    extract_xml_nsmap,
    get_element_by_xpath,
    get_elements_by_xpath,
    create_literal,
    create_uri_from_node_tag,
    create_uri_from_node_tag_by_custom_sequence,
    uri_handling_condition,
    create_literal_from_coordinates
)


GEO = Namespace("http://www.opengis.net/ont/geosparql#")


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

    def test_012_parse_xml(self):
        xml = parse_xml("./tests/sample.xml")
        self.assertIsInstance(xml, ET._Element)

    def test_013_extract_xml_nsmap(self):
        xml = parse_xml("./tests/sample.xml")
        nsmap = extract_xml_nsmap(xml)
        self.assertIsInstance(nsmap, dict)
        self.assertIn("http://www.tei-c.org/ns/1.0", nsmap['xmlns'])

    def test_014_get_element_by_xpath(self):
        xml = parse_xml("./tests/sample.xml")
        element = get_element_by_xpath(xml, "//xmlns:person")
        self.assertIsInstance(element, ET._Element)
        self.assertIn("DWpers0091", element.attrib['{http://www.w3.org/XML/1998/namespace}id'])

    def test_015_get_elements_by_xpath(self):
        xml = parse_xml("./tests/sample.xml")
        elements = get_elements_by_xpath(xml, "//xmlns:person")
        self.assertIsInstance(elements, list)
        self.assertEqual(len(elements), 4)

    def test_016_create_literal(self):
        xml = parse_xml("./tests/sample.xml")
        element = get_element_by_xpath(xml, "//xmlns:persName")
        literal = create_literal(
            node=element,
            prefix="His name is: ",
            default_lang="und",
            enforce_default_lang=True
        )
        self.assertIsInstance(literal, Literal)
        self.assertEqual(literal.value, "His name is: Gulbransson, Olaf Leonhard")

    def test_017_create_uri_from_node_tag(self):
        xml = parse_xml("./tests/sample.xml")
        element = get_element_by_xpath(xml, "//xmlns:person")
        uri = create_uri_from_node_tag(
            node=element,
            prefix="http://example.com/",
            attribute=None
        )
        self.assertIsInstance(uri, URIRef)
        self.assertEqual(uri, URIRef("http://example.com/person"))
        uri = create_uri_from_node_tag(
            node=element,
            prefix="http://example.com/",
            attribute="{http://www.w3.org/XML/1998/namespace}id"
        )
        self.assertIsInstance(uri, URIRef)
        self.assertEqual(uri, URIRef("http://example.com/person/DWpers0091"))
        uri = create_uri_from_node_tag(
            node=element,
            prefix="http://example.com/",
            attribute="{http://www.w3.org/XML/1998/namespace}id",
            number=1
        )
        self.assertIsInstance(uri, URIRef)
        self.assertEqual(uri, URIRef("http://example.com/person/DWpers0091/1"))
        uri = create_uri_from_node_tag(
            node=element,
            prefix="http://example.com/",
            attribute="{http://www.w3.org/XML/1998/namespace}id",
            number=1,
            generate_uuid=True
        )
        self.assertIsInstance(uri, URIRef)
        self.assertIn(URIRef("http://example.com/person/DWpers0091"), uri)

    def test_018_create_uri_from_node_tag_by_custom_sequence(self):
        xml = parse_xml("./tests/sample.xml")
        element = get_element_by_xpath(xml, "//xmlns:person")
        uri = create_uri_from_node_tag_by_custom_sequence(
            node=[element, 3],
            prefix=["http://example.com/", 0],
            attribute=["{http://www.w3.org/XML/1998/namespace}id", 1],
            number=[2, 2]
        )
        self.assertIsInstance(uri, URIRef)
        self.assertEqual(uri, URIRef("http://example.com/DWpers0091/2/person"))

    def test_019_uri_handling_condition(self):
        xml = parse_xml("./tests/sample.xml")
        elements = get_elements_by_xpath(xml, "//xmlns:placeName")
        result = []
        for x in elements:
            condition = uri_handling_condition(
                node=x,
                condition_attribute="type",
                condition_value="orig_name"
            )
            self.assertIsInstance(condition, bool)
            if condition:
                result.append(x.text)
        self.assertEqual(result, ["Reval (Tallinn)", "Jaworzno", "Radebeul (?)"])

    def test_020_create_literal_from_coordinates(self):
        xml = parse_xml("./tests/sample.xml")
        element = get_element_by_xpath(xml, "//xmlns:geo")
        literal = create_literal_from_coordinates(
            node=element,
            datatype=GEO['wktLiteral'],
            split_char=" "
        )
        self.assertIsInstance(literal, Literal)
        self.assertEqual(literal, Literal("Point(48.2066 16.37341)", datatype=GEO['wktLiteral']))

    def test_021_extract_begin_end(self):
        xml = parse_xml("./tests/sample.xml")
        element = get_element_by_xpath(xml, "//xmlns:date")
        begin, end = extract_begin_end(node=element)
        self.assertIsInstance(begin, str)
        self.assertIsInstance(end, str)
        self.assertEqual(begin, "1905-07-04")
        self.assertEqual(end, "2000")
