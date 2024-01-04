import uuid
from typing import TypedDict, Union
from lxml.etree import Element, XMLParser
from lxml import etree as ET
from rdflib import Literal, URIRef, Namespace
from acdh_tei_pyutils.utils import make_entity_label
from acdh_graph_pyutils.string_utils import normalize_string


GEO = Namespace("http://www.opengis.net/ont/geosparql#")

Nsmap = TypedDict('Nsmap', {
    "key": str,
})

DATE_ATTRIBUTE_DICT = {
    "notBefore": "start",
    "notBefore-iso": "start",
    "from": "start",
    "from-iso": "start",
    "notAfter": "end",
    "notAfter-iso": "end",
    "to": "end",
    "to-iso": "end",
    "when": "when",
    "when-iso": "when"
}


def extract_begin_end(
    node: Union[Element, dict],
    fill_missing: bool = True,
    attribute_map: dict = DATE_ATTRIBUTE_DICT,
) -> tuple[Union[str, bool], Union[str, bool]]:
    """
    Returns a tuple of two strings (begin, end) from a date object.
    """
    final_start, final_end = None, None
    start, end, when = None, None, None
    for key, value in attribute_map.items():
        date_value = node.get(key)
        if date_value and value == "start":
            start = date_value
        if date_value and value == "end":
            end = date_value
        if date_value and value == "when":
            when = date_value
    if fill_missing:
        if start or end or when:
            if start and end:
                final_start, final_end = start, end
            elif start and not end and not when:
                final_start, final_end = start, start
            elif end and not start and not when:
                final_start, final_end = end, end
            elif when and not start and not end:
                final_start, final_end = when, when
            elif when and end and not start:
                final_start, final_end = when, end
    else:
        if start and end:
            final_start, final_end = start, end
        elif start and not end and not when:
            final_start, final_end = start, None
        elif end and not start and not when:
            final_start, final_end = None, end
        elif when and not start and not end:
            final_start, final_end = when, when
        elif when and end and not start:
            final_start, final_end = when, end
    return final_start, final_end


def parse_xml(
    xml_file: str
) -> Element:
    """
    Returns an lxml.etree.ElementTree object.
    """
    p = XMLParser(huge_tree=True)
    return ET.parse(xml_file, parser=p).getroot()


def extract_xml_nsmap(
    input: Element,
) -> dict:
    """
    Returns a dict with the namespaces of the input XML file.
    """
    nsmap = input.nsmap.copy()
    nsmap['xmlns'] = nsmap.pop(None)
    return nsmap


def get_element_by_xpath(
    node: Element,
    xpath: str,
) -> Element:
    """
    Returns an lxml.etree.Element object.
    """
    nsmap = extract_xml_nsmap(node)
    return node.xpath(xpath, namespaces=nsmap)[0]


def get_elements_by_xpath(
    node: Element,
    xpath: str,
) -> list[Element]:
    """
    Returns a list of lxml.etree.Element objects.
    """
    nsmap = extract_xml_nsmap(node)
    return node.xpath(xpath, namespaces=nsmap)


def create_literal(
    node: Element,
    prefix: str,
    default_lang: str | bool = False,
    enforce_default_lang: bool = False,
) -> Literal:
    """
    Extracts text from a provided lxml.etree.Element and
    returns a rdflib Literal object.
    """
    if enforce_default_lang:
        lang = default_lang
    else:
        try:
            lang = node.attrib["{http://www.w3.org/XML/1998/namespace}lang"]
        except KeyError:
            lang = "und"
    if len(node.xpath("./*")) < 1 and node.text:
        if default_lang:
            literal = Literal(f"{prefix}{normalize_string(node.text)}", lang=lang)
        else:
            literal = Literal(f"{prefix}{normalize_string(node.text)}")
    elif len(node.xpath("./*")) >= 1:
        entity_label_str, cur_lang = make_entity_label(node, default_lang=lang)
        if default_lang:
            literal = Literal(f"{prefix}{normalize_string(entity_label_str)}", lang=lang)
        else:
            literal = Literal(f"{prefix}{normalize_string(entity_label_str)}")
    else:
        literal = Literal("undefined")
    return literal


def create_uri_from_node_tag(
    node: Element,
    prefix: str,
    number: int = None,
    attribute: str = "{http://www.w3.org/XML/1998/namespace}id",
    generate_uuid: bool = False,
) -> URIRef:
    """
    Extracts node.tag and [optional] node.attribute from a provided lxml.etree.Element and
    returns a rdflib URIRef object.
    """
    node_tag = node.tag.split("}")[-1].lower()
    if prefix.endswith("/"):
        prefix = prefix[:-1]
    uri_parts = [prefix, node_tag]
    if attribute:
        node_id = node.attrib[attribute]
        uri_parts.append(node_id)
    if generate_uuid:
        uri_parts.append(str(uuid.uuid4()))
    if number:
        uri_parts.append(str(number))
    uri = "/".join([x for x in uri_parts if x != "" and x is not None])
    return URIRef(uri)


def create_uri_from_node_tag_by_custom_sequence(
    node: list[Element, int] = [False, False],
    prefix: list[str, int] = [False, False],
    number: list[int, int] = [False, False],
    attribute: list[str, int] = ["{http://www.w3.org/XML/1998/namespace}id", False],
    generate_uuid: list[bool, int] = [False, False],
) -> URIRef:
    """
    Extracts node.tag and [optional] node.attribute from a provided lxml.etree.Element.
    [Optional] number and [optional] uuid can be added to the URI.
    Returns a rdflib URIRef object.
    """
    arguments = locals()
    node_tag = node[0].tag.split("}")[-1].lower()
    if prefix[0] and prefix[0].endswith("/"):
        prefix = prefix[0][:-1]
    if attribute[0]:
        attribute = node[0].attrib[attribute[0]]
    if generate_uuid[0]:
        custom_id = str(uuid.uuid4())
    if number[0]:
        num = str(number[0])
    # find sequence of arguments [uri_parts] to generate uri
    arguments_dict = {value[1]: key for key, value in arguments.items() if value is not False and value[1] is not False}
    sorted_arguments_dict = dict(sorted(arguments_dict.items()))
    uri_parts = []
    for x in sorted_arguments_dict.values():
        if x == "node":
            uri_parts.append(node_tag)
        if x == "prefix":
            uri_parts.append(prefix)
        if x == "attribute":
            uri_parts.append(attribute)
        if x == "generate_uuid":
            uri_parts.append(custom_id)
        if x == "number":
            uri_parts.append(num)
    uri = "/".join([x for x in uri_parts if x != "" and x is not None])
    return URIRef(uri)


def uri_handling_condition(
    node: Element,
    condition_attribute: str,
    condition_value: str,
) -> bool:
    """
    Returns a boolean value based on a condition.
    """
    if condition_attribute in node.attrib.keys():
        if node.attrib[condition_attribute] == condition_value:
            return True
    return False


def create_literal_from_coordinates(
    node: Element,
    datatype: URIRef = GEO['wktLiteral'],
    split_char: str = " ",
) -> Literal:
    """
    Extracts text from a provided lxml.etree.Element,
    splits the text by a given char and
    returns a rdflib Literal object of a specific datatype.
    """
    longitude = node.text.split(split_char)[0]
    latitude = node.text.split(split_char)[1]
    return Literal(f"Point({longitude} {latitude})", datatype=datatype)
