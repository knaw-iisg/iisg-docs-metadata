# Harvesting IISG metadata with OAI-PMH

The [Open Archives Initiative Protocol for Metadata Harvesting](https://www.openarchives.org/OAI/openarchivesprotocol.html)
(OAI-PMH) is a small HTTP protocol for copying a repository's metadata in bulk.
It has six *verbs*. You send one as a URL parameter, and the reply is always
an XML document.

The IISG endpoint is:

```
https://api.socialhistoryservices.org/solr/all/oai
```

It holds over 1.2 million library records, more than 600,000 authority
records, about 5,500 archives and collections, and audiovisual and
visual-material collections. For the full list of sets and formats, see the
[endpoint reference](../reference/oai-pmh.md).

!!! info "Looking for a web page, not XML?"
    OAI-PMH is for harvesting scripts. Every link on this page returns raw
    XML, and your browser just shows the XML tree. To *read* a record as a
    web page, use the [knowledge base viewer]({{ kb_viewer }}) (experimental).
    The example record used below looks like
    [this in the viewer]({{ kb_viewer }}/#https%3A%2F%2Fiisg.amsterdam%2Fid%2Fitem%2F1292895).

!!! danger "Fair use: Harvest responsibly to keep access"
    The OAI-PMH endpoint is a shared service with limited capacity. It also
    serves IISG's own catalogue and search. To keep it available for
    everyone:

    - Send **one request at a time**. Never harvest in parallel, and wait
      for each response before sending the next request.
    - **Back off** on errors and time-outs. Don't retry in a tight loop.
    - Do a full harvest **once**, then use [incremental harvesting](#step-7-harvest-incrementally)
      with `from`. Don't re-download everything every day.
    - Set a `User-Agent` header with your name or project and a contact
      address, so we can reach you before we have to block you.

    Clients that overload the endpoint **will be blocked without notice**.
    If you need more than this, for example a full copy more often than once
    a month, write to [data@iisg.nl](mailto:data@iisg.nl) first.

## When to use OAI-PMH

**Use it** to:

- download a whole set, such as all archive descriptions;
- keep a local copy in sync by fetching only what changed since your last run;
- feed an aggregator, a discovery system, or your own ETL pipeline. The IISG
  knowledge graph is itself built this way.

**Don't use it** to:

- *search*. OAI-PMH has no full-text or field queries. For questions across
  records, use the [SPARQL endpoint](../reference/iris.md#sparql-endpoint).
- look up a single record you already know. `GetRecord` works, but the
  [knowledge base viewer]({{ kb_viewer }}) (experimental) is easier for
  people.

## How a harvest works

```
Identify ─▶ ListSets ─▶ ListMetadataFormats ─▶ ListRecords ──▶ resumptionToken ─┐
                                                   ▲                             │
                                                   └─────── next page ───────────┘
later:  ListRecords + from=<last harvest>   (only what changed)
```

1. `Identify` describes the repository.
2. `ListSets` and `ListMetadataFormats` show what you can ask for.
3. `ListRecords` returns the first 200 records, plus a **resumption token**.
4. Send the token back to get the next 200. Repeat until no token comes back.
5. Next time, add `from` to get only the records that changed.

You can follow every step below in a browser or with `curl`.

## Step 1: Identify the repository

```
https://api.socialhistoryservices.org/solr/all/oai?verb=Identify
```

```xml
<Identify>
  <repositoryName>International Institute of Social History</repositoryName>
  <protocolVersion>2.0</protocolVersion>
  <adminEmail>…</adminEmail>
  <earliestDatestamp>2011-06-01T12:00:00Z</earliestDatestamp>
  <deletedRecord>transient</deletedRecord>
  <granularity>YYYY-MM-DDThh:mm:ssZ</granularity>
  ...
</Identify>
```

Three of these values matter for harvesting:

- **`granularity`**: `from` and `until` accept full UTC timestamps, not just
  dates.
- **`earliestDatestamp`**: nothing is older than June 2011, so you never
  need `from` before that.
- **`deletedRecord: transient`**: the endpoint *may* report deletions, but
  doesn't promise to keep them. A local mirror should do a full re-harvest
  now and then to catch records that disappeared.

For questions about the endpoint, write to [data@iisg.nl](mailto:data@iisg.nl).

## Step 2: Explore the sets

```
https://api.socialhistoryservices.org/solr/all/oai?verb=ListSets
```

A *set* is a named slice of the repository. Each set has a `setSpec`, the
value you pass as `set=`, and a readable `setName`:

```xml
<set>
  <setSpec>iish.archieven</setSpec>
  <setName>Archives</setName>
</set>
```

Most people need one of these:

| `setSpec` | What's in it |
|---|---|
| `iish.evergreen.biblio` | Library catalogue: books, brochures, serials, posters, photos, objects |
| `iish.archieven` | Archives and collections (one record per archive) |
| `iish.evergreen.authority` | Authority records: persons, organisations, places, topics |
| `iish.eci` | Audio and visual material |

Sets are hierarchical: `iish.evergreen.biblio` is part of `iish.evergreen`,
which is part of `iish`. A record's header lists every set it belongs to.

## Step 3: Pick a metadata format

```
https://api.socialhistoryservices.org/solr/all/oai?verb=ListMetadataFormats
```

Every record is available in several formats. Choose one with
`metadataPrefix`:

| Prefix | When to use it |
|---|---|
| `oai_dc` | Quick overview; flat Dublin Core, easy to parse |
| `marcxml` | Full catalogue record. Use this for library and authority records |
| `ead` | Full archival description with the inventory (finding aid). Use this for `iish.archieven` |
| `mods` | Library records in MODS |

`oai_dc` is lossy: subfields and roles are merged into one string. If you
need structure (who was the *creator*, which subject is a *place*), use
`marcxml` or `ead`.

## Step 4: Harvest records

Fetch the first page of the archives set as Dublin Core:

```
https://api.socialhistoryservices.org/solr/all/oai?verb=ListRecords&metadataPrefix=oai_dc&set=iish.archieven
```

To list only the identifiers and datestamps, without the metadata, use
`ListIdentifiers` with the same parameters. It's much faster when you only
need to know *what* exists or changed.

## Step 5: Read the XML

Every record has a **header** and a **metadata** block:

```xml
<record>
  <header>
    <identifier>oai:socialhistoryservices.org:1292895</identifier>
    <datestamp>2022-03-08T13:09:05.799Z</datestamp>
    <setSpec>iish.evergreen.biblio</setSpec>
    <setSpec>VIS-NonEuropeanMovement</setSpec>
  </header>
  <metadata>
    <oai_dc:dc>
      <dc:title>[Textile.]Visual document.</dc:title>
      <dc:date>1983.</dc:date>
      <dc:subject>Women.(NL-AMISG)264172</dc:subject>
      <dc:coverage>South Africa.(NL-AMISG)287153</dc:coverage>
      <dc:contributor>Anti-Apartheidsbeweging Nederland (Amsterdam).Vrouwengroep.(NL-AMISG)20389</dc:contributor>
    </oai_dc:dc>
  </metadata>
</record>
```

- **`identifier`** is stable. Use it as your key. It is also how you find the
  record in the knowledge graph (see [Step 9](#step-9-follow-a-record-into-the-knowledge-graph)).
- **`datestamp`** is when the record last changed. Library records include
  milliseconds (`.799Z`), even though `Identify` advertises second
  granularity. Parse datestamps leniently.
- **`(NL-AMISG)264172`** at the end of a value is a pointer to an IISG
  authority record: here, the topic *Women*. In the knowledge graph it is a
  real link, `https://iisg.amsterdam/authority/topic/264172`.

## Step 6: Page through results

A page holds 200 records. If there is more, the response ends with a
resumption token:

```xml
<resumptionToken cursor="0" completeListSize="1228357"
                 expirationDate="2026-10-30T08:07:39Z">TGlzdFJl…</resumptionToken>
```

Request the next page with the verb and the token **only**:

```
?verb=ListRecords&resumptionToken=TGlzdFJl…
```

- `completeListSize` tells you how many records the whole harvest has.
- Tokens expire after about 24 hours, so don't pause a harvest overnight.
- The last page has an empty `<resumptionToken/>`, or none at all.
- The protocol forbids sending other arguments with a token. This endpoint
  tolerates them, but other OAI servers don't, so leave them out.

## Step 7: Harvest incrementally

To stay in sync, keep the time you started your last harvest and ask only for
records changed since then:

```
?verb=ListRecords&metadataPrefix=marcxml&set=iish.archieven&from=2026-10-01T00:00:00Z
```

Add `until` to close the window. Timestamps are in UTC
(`YYYY-MM-DDThh:mm:ssZ`).

When nothing changed, the answer is not an empty list but an error:

```xml
<error code="noRecordsMatch"/>
```

That's normal. Treat `noRecordsMatch` as "zero records", not as a failure.

## Step 8: Python examples

The examples use [`requests`](https://requests.readthedocs.io) and the
standard library:

```bash
pip install requests
```

### Basic example: one page

Print identifier, datestamp and title for the first 200 archives:

```python
--8<-- "examples/oai_basic.py"
```

### A complete harvest

!!! warning "Remember the fair-use rules"
    The script below sends one request at a time and waits a second between
    pages. Don't remove that pause, and don't run several copies at once:
    clients that overload the endpoint are blocked. The full library set is
    more than 6,000 pages, so plan for hours, not minutes. Then switch to
    `--from`.

This script follows resumption tokens, retries on time-outs, handles
`noRecordsMatch`, and writes each page to disk. It supports `--from` for
incremental runs.

```python
--8<-- "examples/oai_harvest.py"
```

```bash
python oai_harvest.py iish.archieven ead archives/
python oai_harvest.py iish.archieven ead archives-delta/ --from 2026-10-01T00:00:00Z
```

## Step 9: Follow a record into the knowledge graph

An OAI record gives you text: `Women.(NL-AMISG)264172`. The IISG knowledge
graph is built nightly from this same endpoint. It turns those pointers into
links you can follow, and joins library, archive and authority records with
other sources such as IIIF images and Dataverse datasets.

Every OAI identifier maps to one IRI (see the [IRI reference](../reference/iris.md)):

| OAI identifier | Knowledge-graph IRI |
|---|---|
| `oai:socialhistoryservices.org:1292895` | `https://iisg.amsterdam/id/item/1292895` |
| `oai:socialhistoryservices.org:10622/ARCH02487` | `https://iisg.amsterdam/id/collection/ARCH02487` |

This script takes a harvested record, works out its IRI, and asks the SPARQL
endpoint what it links to. It sends one query per record, so for a whole set,
write one SPARQL query over the graph instead of looping over records.

```python
--8<-- "examples/oai_to_sparql.py"
```

Output (shortened):

```
oai:socialhistoryservices.org:1292895 (datestamp 2022-03-08T13:09:05.799Z)
  -> https://iisg.amsterdam/id/item/1292895

  http://id.loc.gov/vocabulary/relators/cre
      https://iisg.amsterdam/authority/organization/20389  Anti-Apartheidsbeweging Nederland (Amsterdam)
  https://schema.org/about
      https://iisg.amsterdam/authority/place/287153  South Africa
  https://iisg.amsterdam/vocab/topic
      https://iisg.amsterdam/authority/topic/264172  Women
  https://schema.org/contentUrl
      https://access.iisg.amsterdam/universalviewer/#?manifest=https://hdl.handle.net/10622/N30051002846324?locatt=view:manifest
```

The `(NL-AMISG)` pointers are now typed links: an organisation as creator, a
place, a topic. The topic itself links on to the Library of Congress subject
heading (`sdo:sameAs`). You can also open the IRI in the experimental
[viewer]({{ kb_viewer }}) to browse the same links.

## Summary

| Task | Request |
|---|---|
| About the repository | `?verb=Identify` |
| Available sets | `?verb=ListSets` |
| Available formats | `?verb=ListMetadataFormats` |
| Records in a set | `?verb=ListRecords&metadataPrefix=marcxml&set=iish.evergreen.biblio` |
| Identifiers only | `?verb=ListIdentifiers&metadataPrefix=oai_dc&set=iish.archieven` |
| Next page | `?verb=ListRecords&resumptionToken=…` |
| Changes since a date | add `&from=2026-10-01T00:00:00Z` |
| One record | `?verb=GetRecord&metadataPrefix=ead&identifier=oai:socialhistoryservices.org:10622/ARCH02487` |
