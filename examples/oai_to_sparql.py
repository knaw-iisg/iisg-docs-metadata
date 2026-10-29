"""Take an OAI-PMH record, derive its IRI in the IISG knowledge graph, and
ask the SPARQL endpoint for the names of everything it links to."""

import requests
import xml.etree.ElementTree as ET

ENDPOINT = "https://api.socialhistoryservices.org/solr/all/oai"
SPARQL = "https://sparql.zijdeman.nl"
NS = {"oai": "http://www.openarchives.org/OAI/2.0/"}
OAI_PREFIX = "oai:socialhistoryservices.org:"


def kg_iri(oai_identifier):
    """Map an OAI identifier to the IRI the IISG ETL pipelines mint for it.

    oai:socialhistoryservices.org:1292895           -> .../id/item/1292895
    oai:socialhistoryservices.org:10622/ARCH02487   -> .../id/collection/ARCH02487
    """
    local = oai_identifier.removeprefix(OAI_PREFIX)
    if local.startswith("10622/"):
        return "https://iisg.amsterdam/id/collection/" + local.split("/", 1)[1]
    return "https://iisg.amsterdam/id/item/" + local


QUERY = """
PREFIX sdo: <https://schema.org/>
SELECT ?property ?value ?label WHERE {
  <%s> ?property ?value .
  OPTIONAL { ?value sdo:name ?label }
  FILTER(isIRI(?value))
}
"""

identifier = "oai:socialhistoryservices.org:1292895"
xml = requests.get(
    ENDPOINT,
    params={"verb": "GetRecord", "metadataPrefix": "oai_dc", "identifier": identifier},
    timeout=60,
).content
datestamp = ET.fromstring(xml).findtext(".//oai:datestamp", namespaces=NS)

iri = kg_iri(identifier)
print(f"{identifier} (datestamp {datestamp})\n  -> {iri}\n")

resp = requests.get(
    SPARQL,
    params={"query": QUERY % iri},
    headers={"Accept": "application/sparql-results+json"},
    timeout=60,
)
resp.raise_for_status()
for row in resp.json()["results"]["bindings"]:
    label = row.get("label", {}).get("value", "")
    print(f"  {row['property']['value']}\n      {row['value']['value']}  {label}")
