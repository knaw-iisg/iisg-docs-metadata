"""Harvest every record of a set, following resumption tokens, and write
each page of raw XML to disk.

Usage:
    python oai_harvest.py iish.archieven marcxml out/
    python oai_harvest.py iish.archieven marcxml out/ --from 2026-10-01T00:00:00Z
"""

import argparse
import time
from pathlib import Path

import requests
import xml.etree.ElementTree as ET

ENDPOINT = "https://api.socialhistoryservices.org/solr/all/oai"
NS = {"oai": "http://www.openarchives.org/OAI/2.0/"}
# Tell IISG who you are, so they can contact you instead of blocking you.
USER_AGENT = "my-project-harvester/1.0 (you@example.org)"
PAUSE_SECONDS = 1  # between pages; keep this, the endpoint is shared


def get(session, params, retries=5):
    """GET with a simple linear back-off; large harvests do hit timeouts."""
    for attempt in range(retries):
        try:
            resp = session.get(ENDPOINT, params=params, timeout=120)
            resp.raise_for_status()
            return resp.content
        except requests.RequestException:
            if attempt == retries - 1:
                raise
            time.sleep(3 * (attempt + 1))


def harvest(set_spec, prefix, out_dir, from_=None, max_pages=None):
    out_dir.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    params = {"verb": "ListRecords", "metadataPrefix": prefix, "set": set_spec}
    if from_:
        params["from"] = from_

    page = 0
    while True:
        root = ET.fromstring(get(session, params))

        error = root.find("oai:error", NS)
        if error is not None:
            # noRecordsMatch is the normal answer to an empty incremental harvest.
            print(f"OAI error {error.get('code')}: {error.text or ''}".strip())
            return

        page += 1
        (out_dir / f"page-{page:05d}.xml").write_bytes(ET.tostring(root))

        token = root.find(".//oai:resumptionToken", NS)
        if page == 1 and token is not None:
            print(f"{token.get('completeListSize')} records to harvest")
        if token is None or not (token.text or "").strip():
            break
        if max_pages and page >= max_pages:
            break
        # A resumptionToken request carries the verb and the token, nothing else.
        params = {"verb": "ListRecords", "resumptionToken": token.text.strip()}
        time.sleep(PAUSE_SECONDS)

    print(f"wrote {page} page(s) to {out_dir}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("set_spec")
    ap.add_argument("prefix")
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--from", dest="from_")
    ap.add_argument("--max-pages", type=int)
    args = ap.parse_args()
    harvest(args.set_spec, args.prefix, args.out_dir, args.from_, args.max_pages)
