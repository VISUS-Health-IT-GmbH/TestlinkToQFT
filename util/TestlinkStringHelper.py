import re

"""
Utility file that contains functions to convert and parse Strings
"""


def clean_html_tags(text: str) -> str:
    """
    Replaces html tags from TL API response with proper text
    :param text: String containing text to be cleaned
    :returns: clean text
    """
    # 1) Per RegEx HTML-Tags entfernen
    clean_text = re.sub('<[^<]+?>', '', text)
    return clean_text


def clean_html_entities(text: str) -> str:
    """
    Replaces html entities from TL API response with proper text
    :param text: String containing text to be cleaned
    :returns: clean text
    """

    # 1) Typ explizit abfangen
    if type(text) is str:
        # 2) XML/HTML-Entities ersetzen
        clean_text = text.replace("&auml;",
                                  "ä").replace("&ouml;",
                                  "ö").replace("&uuml;",
                                  "ü").replace("&Auml;",
                                  "Ä").replace("&Ouml;",
                                  "Ö").replace("&Uuml;",
                                  "Ü").replace("&szlig;",
                                  "ß").replace("&quot;",
                                  "\"").replace("&amp;",
                                  "&").replace("&bdquo;",
                                  "\"").replace("&ldquo",
                                  "\"").replace("&nbsp;",
                                  " ")

        # 3) Rückgabe
        return clean_text

    else:
        return text


def parse_tc_name(tl_tc_response: dict) -> str:
    """
    Converts testcase id and name from response to standardized name format for .qft-file \n
    Format = $ID_§Name, no spaces
    """
    # 1) Name aus dem Dictionary auslesen
    clean_tc_id = tl_tc_response["full_tc_external_id"].replace("-", "").replace(" ", "")

    # 2) Externe Testfall-ID aus dem Dictionary auslesen
    # 2a) Hier müssen alle möglichen Testfallnamensformate abgefangen werden (a-b, a - b, a_b, a _ b, a__b usw.)
    clean_tc_name = tl_tc_response["name"].replace("-", "_")\
                                            .replace(" ", "_")\
                                            .replace("___", "_")\
                                            .replace("__", "_")
    return clean_tc_id + "_" + clean_tc_name

