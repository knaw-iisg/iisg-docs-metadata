# iisg-docs-metadata

User documentation for IISG's data services (OAI-PMH, SPARQL / knowledge
graph), built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
and published to GitHub Pages on every push to `main`.

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
