# OAI-PMH endpoint reference

| | |
|---|---|
| Base URL | `https://api.socialhistoryservices.org/solr/all/oai` |
| Protocol | OAI-PMH 2.0 |
| Verbs | `Identify`, `ListSets`, `ListMetadataFormats`, `ListIdentifiers`, `ListRecords`, `GetRecord` |
| Page size | 200 records |
| Resumption token lifetime | ~24 hours |
| Datestamp granularity | `YYYY-MM-DDThh:mm:ssZ` (UTC) |
| Earliest datestamp | `2011-06-01T12:00:00Z` |
| Deleted records | `transient` |
| Identifier scheme | `oai:socialhistoryservices.org:<local id>` |
| Contact | [data@iisg.nl](mailto:data@iisg.nl) |

!!! danger "Fair use"
    This is a shared service with limited capacity. Send **one request at a
    time**, never in parallel, and wait for each response before sending the
    next. Back off when you get errors or time-outs. Clients that overload
    the endpoint **will be blocked without notice**. If you need a full copy
    more often than once a month, write to [data@iisg.nl](mailto:data@iisg.nl)
    first.

## Metadata formats

| `metadataPrefix` | Schema | Notes |
|---|---|---|
| `oai_dc` | Dublin Core | Available for every record; flattens structure |
| `marcxml` | MARC 21 slim | Library, serial, archive-level and authority records |
| `ead` | EAD 2002 | Archival finding aids (`iish.archieven`) |
| `mods` | MODS 3 | Library records |
| `eci` | EAD-based | Audiovisual collection records (`iish.eci`) |
| `rdfvufind`, `rdfsimili`, `solr` | | Internal formats used by IISG systems; not recommended for reuse |

## Sets

Record counts were taken from `completeListSize` in October 2026 and change
daily.

| `setSpec` | Name | Records |
|---|---|---:|
| `iish.evergreen.biblio` | Library catalogue | 1,228,357 |
| `iish.evergreen.authority` | Authority list | 615,693 |
| `iish.archieven` | Archives | 5,557 |
| `iish.eci` | Audio and visual material | 919 |
| `serials` | Serials | |
| `IISG` | IISG collections | 75,338 |
| `PM` | Persmuseum (also `PM.archive`, `PM.biblio`, `PM.HahnAlbert`) | 53,762 |
| `nondig` | Records without digital content (also `nondig.serials`, `nondig.books_and_brochures`, …) | 966,611 |
| `VIS-DutchLabourMovements` | Dutch labour movements | |
| `VIS-ParadisoMelkweg` | Posters Paradiso and Melkweg | |
| `VIS-AHP` | Algemeen Hollands Fotopersburo | |
| `VIS-DutchPoliticalSocialMovements` | Posters Dutch political and social movements 1890–1995 | |
| `VIS-EuropeanSocialMovements` | Social movements 19th–20th century, photos and posters | |
| `VIS-NonEuropeanMovement` | Social movements 19th–20th century, photos and posters | |

`iish.archivesspace.marc` and `irsh` are listed by `ListSets` but currently
return `noRecordsMatch`.

## Identifier patterns

| Record type | OAI identifier example |
|---|---|
| Library record | `oai:socialhistoryservices.org:1292895` |
| Archive / collection | `oai:socialhistoryservices.org:10622/ARCH02487` |
| Serial | `oai:socialhistoryservices.org:10622/Z94825` |
| Authority | `oai:socialhistoryservices.org:iish.evergreen.authority:229111` |

## Errors

| Code | Meaning here |
|---|---|
| `noRecordsMatch` | Empty result, e.g. no changes since `from`, or an unknown or empty set. Not a failure. |
| `badResumptionToken` | Token expired or mangled. Restart the harvest, using `from` to skip what you already have. |
| `cannotDisseminateFormat` | Unknown `metadataPrefix`. |

!!! warning "Format fallback"
    Asking for a known format a record doesn't have does *not* raise
    `cannotDisseminateFormat`. For example, `ead` on a library record
    returns the MARC record instead. Check the root element of
    `<metadata>` if your harvester mixes sets and formats.
| `idDoesNotExist` | `GetRecord` with an unknown identifier. |
