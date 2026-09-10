# ANN/A M2 persistent experience implementation — 2026-08-29

## Result

M2 is implemented and passes its synthetic/reopen gates.  It has not been
retroactively seeded from previously processed material.

The single-material path can now continue one durable shared AV learning state
across separate executions.  It no longer creates empty audio and visual
ledgers when `--experience-ledger` is supplied.

## What changed

- Added one append-only, SHA-256 chained shared AV experience ledger.
- One shared coordinate atomically commits audio, visual, audio-temporal, and
  visual-temporal revision deltas in one record.
- Each new execution verifies and reconstructs both modality states before the
  reader starts.
- After ingest, the runner performs CRC audit and a second independent reopen.
- Duplicate source hashes are rejected; video duplicates are rejected before
  decode.
- Exact evidence remains audit provenance.
- Exact cross-source key recurrence remains explicitly unnecessary.

## Verification

- targeted persistence/ingest/reader integration: 21/21 passed;
- complete local regression: 267/267 passed;
- two independent synthetic sources successfully continued through separate
  open/read/close/reopen cycles;
- complete-record tampering and torn appends were rejected;
- CRC audit made no writes;
- the shared neutral decoder instantiated with PyAV 15.1.0 from the
  environment-managed Codex primary Python site-packages.

## Material boundary

The six recent M1 videos and their neutral archives were not reread.  Their
ephemeral ledgers cannot be reconstructed honestly from summary reports, so
they were not replayed merely to populate M2.

The first future genuinely new material will create the real persistent
ledger.  Every later new material can then reopen and extend that same state.
That first real run will be M2's operational milestone; current status is
implementation-complete and real-ledger-unseeded.

## Project files

- `ann_persistent_shared_av_experience_v1_0.py`
- `test_ann_persistent_shared_av_experience_v1_0.py`
- updated `run_ann_single_material_ingest_v1_0.py`
- updated `test_run_ann_single_material_ingest_v1_0.py`
- `A_ANN_PERSISTENT_SHARED_AV_EXPERIENCE_V1_0.md`

They are stored in:

`C:\Users\termi\Documents\Codex\2026-08-27\ann-a-a-learning-relation-append\outputs`

