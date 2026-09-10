# ANN/A single-material ingest results — 2026-08-29 10:11–10:34

## Outcome

All three newly supplied MP4 files were decoded once and produced visible,
independent source-local ANN/A responses through the unchanged v1.21 reader.

| Source | State | Duration | Reads | Audio recurrence | Visual recurrence | +2 decisions | Audio structures | Visual structures |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 101128 | observed | 8.70 s | 64 | 17 | 22 | 4 | 53 | 9 |
| 101506 | observed | 10.87 s | 64 | 14 | 6 | 1 | 54 | 21 |
| 103439 | observed | 9.37 s | 64 | 16 | 1 | 0 | 58 | 18 |

Totals across the independent runs:

- shared reads: 192/192;
- audio recurrence observations: 47;
- visual recurrence observations: 29;
- +2 decisions: 5;
- adjacent pairs retained: 184;
- adjacent triples retained: 178.

103439 generated local audio and visual recurrence but no joint recurrence at
one coordinate, so the local-capability reader correctly retained adjacent
`+1` movement for every turn.  That is an explicit policy response, not a
silent or inactive run.

Every report records:

- `material_accepted = true`;
- `source_local_learning_observed = true`;
- `source_local_recurrence_observed = true`;
- `local_capability_effect_observed = true`;
- `exact_cross_source_key_required = false`;
- `cross_source_comparison_performed = false`.

The three source hashes are distinct.  No evidence or ledger was merged across
sources.

## PyAV boundary encountered and resolved

The first 101128 invocation initially stopped before media decode because the
decoder-local runtime was not readable in the new permission turn.  It created
no archive or report.  PyAV 15.1.0 was then installed in the persistent shared
workspace runtime and added ahead of historical project runtimes.  A fresh
process loaded `av.open` from that exact shared path, after which all three
videos decoded successfully once.

## Verification and limits

- complete local regression after the final decoder change: 263/263 passed;
- all three archives and reports exist;
- original videos were not changed, moved, renamed, or deleted;
- this confirms repeatable M1 source-local response and the final cross-turn
  PyAV runtime path;
- it does not yet implement M2 durable append-only experience across separate
  ingest executions;
- it makes no semantic, identity, relationship, or external-generalization
  claim.

Project reports are stored in:

`C:\Users\termi\Documents\Codex\2026-08-27\ann-a-a-learning-relation-append\outputs`

