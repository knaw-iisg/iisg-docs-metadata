# iisg-docs-metadata

User documentation for IISG's data services (OAI-PMH, SPARQL / knowledge
graph).

## 👉 Read the documentation

**<https://knaw-iisg.github.io/iisg-docs-metadata/>**

> [!WARNING]
> **Beta.** This documentation is new and still changing.
>
> IISG's official SPARQL endpoint is **<https://iisg.amsterdam/kg>**. For
> testing purposes, the documentation and its examples use another endpoint
> (`https://sparql.zijdeman.nl`), which runs a newer version of the graph.
> The IRIs are the same, but not every example gives the same results on
> the official endpoint. The knowledge base viewer (`https://kb.zijdeman.nl`)
> is experimental too.

This repository holds the *source* of that website. The Markdown files in
`docs/` are turned into the HTML site automatically on every push to `main`.
Start with the [OAI-PMH tutorial](https://knaw-iisg.github.io/iisg-docs-metadata/tutorials/oai-pmh/).

## Where do I see records as web pages?

Not in OAI-PMH. Its responses are raw XML, meant for harvesting scripts,
and a browser just shows the XML tree, e.g.
<https://api.socialhistoryservices.org/solr/all/oai?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:socialhistoryservices.org:1292895>.

To read a record as a web page, with its creators, subjects and places as
clickable links, use the **knowledge base viewer** (experimental, like the
test SPARQL endpoint it runs on): <https://kb.zijdeman.nl>.
Search for anything, or open a record directly by putting its IRI after `#`.
For example, the T-shirt used throughout the tutorial:

<https://kb.zijdeman.nl/#https%3A%2F%2Fiisg.amsterdam%2Fid%2Fitem%2F1292895>

(OAI identifier `oai:socialhistoryservices.org:1292895` → IRI
`https://iisg.amsterdam/id/item/1292895`; see the
[IRI reference](https://knaw-iisg.github.io/iisg-docs-metadata/reference/iris/).)

You can also build your own interface like this. The viewer has no server
of its own: it is a single web page that sends SPARQL queries from the
browser. See [its source](https://github.com/knaw-iisg/iisg-kb-viewer).

## Working on the docs

Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).
To preview your changes locally:

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt requests
.venv/bin/mkdocs serve        # preview at http://127.0.0.1:8000
```

Code samples live in `examples/` and are included into the pages with
`--8<--` snippets, so the site always shows the exact script that was run.
Run them against the live endpoints before changing a tutorial:

```bash
.venv/bin/python examples/oai_basic.py
.venv/bin/python examples/oai_harvest.py iish.archieven marcxml /tmp/h --max-pages 2
.venv/bin/python examples/oai_to_sparql.py
```

Service URLs (SPARQL endpoint, query UI, viewer) are set once under `extra:`
in `mkdocs.yml` and used in the pages as `{{ sparql_endpoint }}`,
`{{ query_ui }}` and `{{ kb_viewer }}`. `examples/oai_to_sparql.py` keeps
a literal copy so it stays runnable on its own; `scripts/check_urls.py`
(run in CI) fails the build if the two drift apart.
