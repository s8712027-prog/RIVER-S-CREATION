# ANN/A single-material ingest response fix — 2026-08-29

## Outcome

The material-to-reader wiring gap is fixed in the ANN/A project.  Previously,
natural and external runners contained hard-coded archive lists.  A video path
supplied in a message or placed in a folder did not invoke ANN/A, so no visible
response could occur.

The new entry point is:

`C:\Users\termi\Documents\Codex\2026-08-27\ann-a-a-learning-relation-append\outputs\run_ann_single_material_ingest_v1_0.py`

It accepts one video or one existing neutral archive and immediately invokes
the unchanged active v1.21 local-capability reader.  It does not wait for a
formation/heldout group and does not require exact cross-source key recurrence.

## Visible states

Every invocation prints and saves one structured report:

- `observed`: source-local recurrence and reader decisions were observed;
- `observed-no-recurrence`: reads completed but this source had not formed a
  local recurrence;
- explicit rejection/error: the source could not supply a complete shared AV
  coordinate or violated an input boundary.

The report exposes read count, modality tiers, decision drivers and offsets,
adjacency retention, source-local temporal-structure counts, and frontier
reach.  It explicitly records:

- `exact_cross_source_key_required: false`;
- `cross_source_comparison_performed: false`;
- `semantic_or_relationship_claim_created: false`.

## Safety

- video mode refuses to overwrite an existing neutral archive;
- report output refuses to overwrite an existing report;
- original media is never moved, renamed, changed, or deleted;
- archive mode performs no video decode;
- this response is observation, not external validation or promotion.

## Verification

- targeted new-entry plus active-reader tests initially passed 15/15;
- a subsequent real decoder-module import smoke check exposed and repaired the
  Python module-registration boundary before any video was opened;
- the decoder import check passes after that repair;
- final complete local unit regression: 262/262 passed;
- no user video or existing neutral archive was opened during verification.

Implementation documentation and tests were added beside the original ANN/A
model files:

- `A_ANN_SINGLE_MATERIAL_INGEST_V1_0.md`;
- `test_run_ann_single_material_ingest_v1_0.py`.

## Remaining product boundary

Attaching a file to a Codex message still does not execute arbitrary project
code automatically.  Codex must invoke the entry point for the supplied path,
or the user may invoke it directly.  Once invoked, one material is sufficient
to receive a visible ANN/A response; no additional source is needed.

