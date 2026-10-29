# IISG Data Services

The [International Institute of Social History](https://iisg.amsterdam) (IISG) holds
archives, library material, serials, posters, photographs and audiovisual
collections on the history of work, workers and social movements. This site
explains how to get that metadata out in bulk and how to query it as Linked Data.

## Beta

!!! warning "Beta"
    **This documentation is new.** Pages, examples and URLs may still
    change. Feedback is welcome at [data@iisg.nl](mailto:data@iisg.nl).

    **The SPARQL endpoint in the examples is a test endpoint.** IISG's
    official knowledge graph is at [{{ official_kg | replace("https://", "") }}]({{ official_kg }}),
    with its SPARQL service at `{{ official_sparql }}`. For testing purposes,
    this documentation uses another endpoint, `{{ sparql_endpoint }}`, which
    runs a newer version of the graph. The IRIs are the same on both, but
    not every example gives the same results on the official endpoint. For
    example, names of topics and places are not yet available there.

    The OAI-PMH endpoint is not affected: it is IISG's production service.

## Which service should I use?

| I want to… | Use |
|---|---|
| Download a whole collection, or keep a local copy in sync | [OAI-PMH](tutorials/oai-pmh.md) |
| Ask questions across collections ("all posters about women's suffrage made in the Netherlands") | [SPARQL endpoint](reference/iris.md#sparql-endpoint) |
| Browse records and their links in a web page | [Knowledge base viewer]({{ kb_viewer }}) |

Both services describe the same records. The OAI-PMH endpoint serves the
catalogue records as the cataloguers made them (MARC, EAD, Dublin Core). The
knowledge graph is rebuilt every night by harvesting that same endpoint,
converting the records to RDF (mainly [schema.org](https://schema.org) and
[RiC-O](https://www.ica.org/standards/RiC/ontology)) and linking them to
persons, organisations, places and topics. The [IRI
reference](reference/iris.md) shows how an OAI identifier becomes a
knowledge-graph IRI.

## Tutorials

- [OAI-PMH](tutorials/oai-pmh.md): explore the endpoint, harvest a set,
  keep it up to date, and follow a record into the knowledge graph.

## Contact

Questions about the OAI-PMH endpoint or the knowledge graph go to
[data@iisg.nl](mailto:data@iisg.nl). To report a problem with this
documentation, open an issue on
[GitHub](https://github.com/knaw-iisg/iisg-docs-metadata/issues).
