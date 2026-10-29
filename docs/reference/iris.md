# Knowledge graph IRIs

The IISG knowledge graph is rebuilt nightly from the
[OAI-PMH endpoint](oai-pmh.md) and other sources. Each OAI record becomes a
resource with a predictable IRI, so you can join your harvested data to the
graph without a lookup table.

## From OAI identifier to IRI

Strip `oai:socialhistoryservices.org:` from the identifier, then:

| OAI local part | IRI | Graph |
|---|---|---|
| `1292895` (library record) | `https://iisg.amsterdam/id/item/1292895` | `https://iisg.amsterdam/graph/biblio` |
| `10622/ARCH02487` (archive) | `https://iisg.amsterdam/id/collection/ARCH02487` | `https://iisg.amsterdam/graph/archive`, `…/graph/findingaid` |
| `iish.evergreen.authority:264172` | `https://iisg.amsterdam/authority/<type>/264172` | `https://iisg.amsterdam/graph/authority` |

Characters that aren't allowed in an IRI path segment are percent-encoded.

## Authority pointers

A value ending in `(NL-AMISG)<id>` in `oai_dc`, or a `$0` subfield with
`(NL-AMISG)<id>` in `marcxml`, points to an authority record. Its IRI
depends on the kind of heading:

| Type | IRI pattern | RDF type |
|---|---|---|
| Person | `https://iisg.amsterdam/authority/person/<id>` | `sdo:Person` |
| Organisation | `https://iisg.amsterdam/authority/organization/<id>` | `sdo:Organization` |
| Event | `https://iisg.amsterdam/authority/event/<id>` | `sdo:Event` |
| Place | `https://iisg.amsterdam/authority/place/<id>` | `sdo:Place` |
| Topic | `https://iisg.amsterdam/authority/topic/<id>` | `sdo:DefinedTerm` |
| Period | `https://iisg.amsterdam/authority/period/<id>` | `sdo:DefinedTerm` |
| Form / genre | `https://iisg.amsterdam/authority/form/<id>` | `sdo:DefinedTerm` |
| Uniform title | `https://iisg.amsterdam/authority/title/<id>` | `sdo:CreativeWorkSeries` |

If you only have the number, ask the graph which type it is:

```sparql
SELECT ?authority ?type WHERE {
  VALUES ?type { "person" "organization" "event" "place" "topic" "period" "form" "title" }
  BIND(IRI(CONCAT("https://iisg.amsterdam/authority/", ?type, "/264172")) AS ?authority)
  ?authority ?p ?o .
}
GROUP BY ?authority ?type
```

## SPARQL endpoint

| | |
|---|---|
| Endpoint | `{{ sparql_endpoint }}` (GET or POST, standard SPARQL 1.1 protocol) |
| Query UI | <{{ query_ui }}> |
| Browser | <{{ kb_viewer }}> |

Main vocabularies: [schema.org](https://schema.org) (`sdo:`),
[RiC-O](https://www.ica.org/standards/RiC/ontology) for archives, MARC
relators (`http://id.loc.gov/vocabulary/relators/`) for roles, and IISG's
own `https://iisg.amsterdam/vocab/` for properties without a standard
equivalent.

Example: library records about the topic *Women*, with their creators:

```sparql
PREFIX sdo: <https://schema.org/>
PREFIX iisgv: <https://iisg.amsterdam/vocab/>
PREFIX rel: <http://id.loc.gov/vocabulary/relators/>

SELECT ?item ?name ?creatorName WHERE {
  ?item iisgv:topic <https://iisg.amsterdam/authority/topic/264172> ;
        sdo:name ?name .
  OPTIONAL { ?item rel:cre/sdo:name ?creatorName }
}
LIMIT 50
```
