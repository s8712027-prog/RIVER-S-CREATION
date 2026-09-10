# ANN/A representation development — 2026-08-28

## Outcome

Two new MP4 sources were explicitly treated as reusable development material.
Each original MP4 was decoded exactly once.  All subsequent work reused the
neutral archives.  Neither the old eleven sources nor the failed three-source
external-validation group was read.

No replacement representation was retained.  The active reader and mainline
representation were not modified.

## Current-representation baseline

The two development sources were split in acquisition order: the first formed
candidates and the second was isolated for comparison.  Each received 64
shared reads.

Audio baseline:

- 60 formation candidates;
- 51 observed structures in the second source;
- 0 supported structures across the split;
- reversed-order matches 2;
- adjacency-broken maximum 3;
- result: Fail.

Visual baseline:

- 7 formation candidates;
- 13 observed structures in the second source;
- 1 supported structure with distinct exact evidence;
- reversed-order matches 2;
- adjacency-broken maximum 0;
- result: Fail because observed support did not exceed reversed order.

The reader completed all reads and remained mostly adjacent.  The failure was
again cross-source structure stability, not timeline traversal.

## Candidate 1 — ordinal directional counts

Change tested:

- replace each exact four-count motif token with the six fixed pairwise
  ordinal relations among the four counts;
- retain fixed anchors, windows, temporal order, admission rules, reader,
  controls, and exact evidence.

Result:

- supported structures increased from 0 to 1;
- 1/1 retained distinct exact evidence;
- reversed-order matches increased to 3;
- adjacency-broken maximum increased to 4;
- decision: reject.

Interpretation: ordinal coarsening increased collisions more than useful
cross-source support.

## Candidate 2 — signed changes between count motifs

Change tested:

- replace the absolute count triple with two signed four-part change
  topologies between its three motifs;
- each component records `up`, `down`, or `same`;
- true reversal reverses token order and inverts `up/down`;
- retain fixed anchors, windows, reader, exact evidence, and adjacency-broken
  controls.

Result:

- formation candidates 31;
- second-source observed structures 36;
- supported structures increased from 0 to 10;
- 10/10 retained distinct exact evidence;
- true reversed-order matches 12;
- adjacency-broken mean 4.903 and maximum 11;
- empirical null upper p-value 0.0625;
- decision: reject.

Interpretation: signed count changes substantially improved cross-source
collision, but did not preserve forward temporal organization strongly enough.
The reverse control exceeded the observation, and an adjacency-broken trial
also exceeded it.

## Test status

Both candidates passed their targeted synthetic invariants together with the
existing scoped-audio and shared-reader tests:

- 23 tests passed for the ordinal candidate run;
- 23 tests passed for the signed-count-change candidate run.

Passing code tests does not override failed empirical controls.

## Mainline decision

- Do not activate either candidate.
- Do not alter local-capability offsets or reader traversal from this evidence.
- Do not add a threshold or gate to make the ten delta matches pass.
- Do not claim external generalization.
- Retain all reports as negative development evidence.

The development result narrows the next representation question: a future
candidate must retain the cross-source stability revealed by count changes
while also preserving forward-direction information that exceeds a correctly
inverted reverse control.  This is a representation problem, not permission to
search more encodings on the same turn.

## Evidence files

- `ann_representation_development_20260828_manifest.json`
- `ann_representation_development_20260828_decode_report.json`
- `ann_representation_development_baseline_20260828_report.json`
- `ann_ordinal_directional_count_development_ab_20260828_report.json`
- `ann_directional_count_delta_development_ab_20260828_report.json`
- `ann_ordinal_directional_count_temporal_v1_40.py`
- `ann_directional_count_delta_temporal_v1_41.py`

The two Python candidates remain isolated development artifacts.  Neither was
wired into `ann_shared_timeline_av_reader_v1_21.py` or the active mainline.

