# ANN/A three single-material ingest results — 2026-08-29 09:51–09:57

## Outcome

All three newly supplied MP4 files were accepted and produced a visible
source-local ANN/A response.  Each file was decoded once into its own neutral
archive and read independently by the unchanged active v1.21
local-capability reader.

| Source | State | Duration | Reads | Audio recurrence | Visual recurrence | +2 decisions | Audio structures | Visual structures |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 095108 | observed | 8.33 s | 64 | 23 | 30 | 9 | 41 | 2 |
| 095413 | observed | 9.00 s | 64 | 22 | 38 | 14 | 37 | 14 |
| 095744 | observed | 9.90 s | 64 | 21 | 41 | 10 | 43 | 14 |

Totals across the three independent runs:

- shared reads: 192/192;
- source-local audio recurrence observations: 66;
- source-local visual recurrence observations: 109;
- local-capability +2 decisions: 33;
- adjacent pairs retained: 157;
- adjacent triples retained: 130.

Every run recorded:

- `material_accepted = true`;
- `source_local_learning_observed = true`;
- `source_local_recurrence_observed = true`;
- `local_capability_effect_observed = true`;
- `exact_cross_source_key_required = false`;
- `cross_source_comparison_performed = false`.

The three container SHA-256 identities are distinct.  Exact identities remain
attached only for provenance audit; no key or learned structure was required
to match another source.

## Runtime repair

The first invocation initially stopped before media decoding because the
historical PyAV directories had unreadable ACLs.  No neutral archive or report
was created by that initialization failure.  An isolated PyAV 15.1.0 runtime
was installed beside the ingest entry point, verified, and the source was then
decoded successfully for the first and only time.

## Verification and boundaries

- final complete local unit regression: 263/263 passed;
- all three neutral archives and reports exist;
- original videos were not modified, moved, renamed, or deleted;
- ledgers were independent per source;
- no semantic, object, identity, relationship, or external-generalization
  claim was created;
- these are visible source-local reader responses, not the frozen external A/B
  required for promotion beyond provisional.

## Project reports

- `ann_ingest_20260829_095108_observe_report.json`
- `ann_ingest_20260829_095413_observe_report.json`
- `ann_ingest_20260829_095744_observe_report.json`

The reports and their neutral archives are stored in:

`C:\Users\termi\Documents\Codex\2026-08-27\ann-a-a-learning-relation-append\outputs`

