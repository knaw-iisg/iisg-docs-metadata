"""Fetch one page of Dublin Core records from the IISG OAI-PMH endpoint
and print identifier, datestamp and title for each record."""

import requests
import xml.etree.ElementTree as ET

ENDPOINT = "https://api.socialhistoryservices.org/solr/all/oai"
NS = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "dc": "http://purl.org/dc/elements/1.1/",
}

params = {
    "verb": "ListRecords",
    "metadataPrefix": "oai_dc",
    "set": "iish.archieven",
}
resp = requests.get(ENDPOINT, params=params, timeout=120)
resp.raise_for_status()
root = ET.fromstring(resp.content)

for record in root.iterfind(".//oai:record", NS):
    identifier = record.findtext("oai:header/oai:identifier", namespaces=NS)
    datestamp = record.findtext("oai:header/oai:datestamp", namespaces=NS)
    title = record.findtext(".//dc:title", default="(no title)", namespaces=NS)
    print(identifier, datestamp, title, sep="\t")
