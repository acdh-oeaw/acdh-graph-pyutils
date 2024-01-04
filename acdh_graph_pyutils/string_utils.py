from typing import Union
from rdflib import Literal, XSD


def normalize_string(string: str) -> str:
    """
    Returns a normalized string.
    """
    return " ".join(" ".join(string.split()).split())


def date_to_literal(
    date_str: Union[str, bool],
    not_known_value="undefined",
    default_lang="en"
) -> Literal:
    """"
    Returns a rdflib Literal object of a date datatype.
    """
    if date_str is None:
        return_value = Literal(not_known_value, lang=default_lang)
    elif date_str == "":
        return_value = Literal(not_known_value, lang=default_lang)
    else:
        if len(date_str) == 4:
            return_value = Literal(date_str, datatype=XSD.gYear)
        elif len(date_str) == 5 and date_str.startswith("-"):
            return_value = Literal(date_str, datatype=XSD.gYear)
        elif len(date_str) == 7:
            return_value = Literal(date_str, datatype=XSD.gYearMonth)
        elif len(date_str) == 10:
            return_value = Literal(date_str, datatype=XSD.date)
        elif len(date_str) == 19:
            return_value = Literal(date_str, datatype=XSD.dateTime)
        elif len(date_str) == 20:
            return_value = Literal(date_str, datatype=XSD.dateTime)
        elif len(date_str) == 25:
            return_value = Literal(date_str, datatype=XSD.dateTime)
        else:
            return_value = Literal(date_str, datatype=XSD.string)
    return return_value
