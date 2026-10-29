"""Fail if examples/oai_to_sparql.py's SPARQL constant differs from
extra.sparql_endpoint in mkdocs.yml, so a domain change can't leave the
example script behind."""

import re
import sys
from pathlib import Path

import yaml

root = Path(__file__).resolve().parent.parent
config = yaml.safe_load((root / "mkdocs.yml").read_text())
expected = config["extra"]["sparql_endpoint"]

script = (root / "examples" / "oai_to_sparql.py").read_text()
match = re.search(r'^SPARQL = "([^"]+)"', script, re.MULTILINE)
actual = match.group(1) if match else None

if actual != expected:
    sys.exit(f"examples/oai_to_sparql.py has SPARQL = {actual!r}, mkdocs.yml has {expected!r}")
print(f"SPARQL endpoint consistent: {expected}")
