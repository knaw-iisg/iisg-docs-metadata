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

    **The knowledge base viewer is experimental too.** The
    [viewer]({{ kb_viewer }}) runs on the same test endpoint. Its address,
    look and features may change.

    The OAI-PMH endpoint is not affected: it is IISG's production service.

## Which service should I use?

| I want to… | Use | Status |
|---|---|---|
| Browse records and their links in a web page | [Knowledge base viewer]({{ kb_viewer }}) | Experimental |
| Build my own web interface or app on top of the data | The [SPARQL endpoint](reference/iris.md#sparql-endpoint). The viewer is an example: [its source](https://github.com/knaw-iisg/iisg-kb-viewer) is a single web page that queries SPARQL straight from the browser | Experimental (test endpoint) |
| Ask questions across collections ("all posters about women's suffrage made in the Netherlands") | [SPARQL endpoint](reference/iris.md#sparql-endpoint) | Experimental (test endpoint) |
| Download a whole collection, or keep a local copy in sync | [OAI-PMH](tutorials/oai-pmh.md) | Production |

All of these describe the same records. The viewer is a web interface on
top of the knowledge graph. It has no server of its own: it sends SPARQL
queries from your browser, so anyone can build a similar interface. The
SPARQL endpoint lets you query that graph directly. The graph itself is rebuilt every night by harvesting the OAI-PMH
endpoint, converting the records to RDF (mainly [schema.org](https://schema.org)
and [RiC-O](https://www.ica.org/standards/RiC/ontology)) and linking them to
persons, organisations, places and topics. OAI-PMH serves the source: the
catalogue records as the cataloguers made them (MARC, EAD, Dublin Core). The
[IRI reference](reference/iris.md) shows how an OAI identifier becomes a
knowledge-graph IRI.

## Tutorials

- [OAI-PMH](tutorials/oai-pmh.md): explore the endpoint, harvest a set,
  keep it up to date, and follow a record into the knowledge graph.

## Contact

Questions about the OAI-PMH endpoint or the knowledge graph go to
[data@iisg.nl](mailto:data@iisg.nl). To report a problem with this
documentation, open an issue on
[GitHub](https://github.com/knaw-iisg/iisg-docs-metadata/issues).
