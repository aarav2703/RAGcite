# arxiv/parser.py

import xml.etree.ElementTree as ET


def parse_arxiv_response(xml_data: str):
    """
    Parses arXiv Atom XML response and extracts useful fields.

    Parameters:
        xml_data (str): Raw XML string from arXiv API.

    Returns:
        List[Dict]: List of dictionaries containing paper metadata.
    """
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml_data)
    papers = []

    for entry in root.findall("atom:entry", ns):
        paper = {
            "title": entry.find("atom:title", ns).text.strip(),
            "summary": entry.find("atom:summary", ns).text.strip(),
            "published": entry.find("atom:published", ns).text.strip(),
            "authors": [
                author.find("atom:name", ns).text
                for author in entry.findall("atom:author", ns)
            ],
            "link": entry.find('atom:link[@type="text/html"]', ns).attrib["href"],
            "pdf_url": entry.find('atom:link[@type="application/pdf"]', ns).attrib[
                "href"
            ],
        }
        papers.append(paper)

    return papers
