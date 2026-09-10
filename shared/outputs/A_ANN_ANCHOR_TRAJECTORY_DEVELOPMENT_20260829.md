# ANN/A link-before-pool anchor trajectory development — 2026-08-29

## Outcome

The frozen v1.43 anchor-trajectory candidate **failed** its single-shot bounded
development test.  This is a Fail, not an Inconclusive result.

The candidate linked each anchor's three ordered directional relations before
pooling, then exactly matched the complete histogram of eight trajectories
without retaining anchor, channel, or source identity.

It produced zero cross-source support:

| Quantity | Result |
|---|---:|
| Formation base coordinates | 62 |
| Held-out base coordinates | 58 |
| Formation admitted occurrences / unique candidates | 60 / 60 |
| Held-out admitted occurrences / unique structures | 51 / 51 |
| Forward supported structures | **0** |
| Representation-reverse matches | 0 |
| Four other time-order controls | all 0 |
| Nine anchor-link-broken controls | all 0 |
| Thirty valid time-adjacency-broken controls | all 0 |
| Maximum frozen control | 0 |
| Control-fairness errors | 0 |
| Decision | **reject-development-candidate** |

Forward ties the controls at zero and does not exceed the exact-count baseline
support of zero.  The preregistered rule therefore requires rejection.

## What was frozen before data access

- Formation: `ann_development_233248_neutral_archive_v0_1.npz`.
- Held-out: `ann_development_233446_neutral_archive_v0_1.npz`.
- Acquisition order fixed the split before representation results were known.
- Read budget: 64 shared-reader turns per source.
- Existing 100 ms windows, eight anchors, four directional relation labels,
  traversal, admission, exact evidence, and active reader remained unchanged.
- No trajectory-length variants, selected bins, thresholds, confidence gates,
  or source labels were allowed.
- Forward and every control started from the same complete constructible
  held-out coordinate set; the unchanged admission was applied independently
  after transformation, with attempted and admitted capacities reported.
- Pass required positive forward support strictly above every individual
  reverse, time-order, anchor-link, and time-adjacency control, with disjoint
  exact evidence and improvement over baseline.

The single-shot attempt marker records the frozen hashes before the first
neutral archive load.  The active reader hash remained:

`74AAA1AF2AACAD0FF8B13DF5DD9D472CBE91F95D07C87F9F773352FF0DD81ACA`.

## Reverse-control scope

The current stereo anchor coordinates are not closed under raw-waveform time
reversal.  All eight audited mirror mappings were unavailable because mirrored
offsets must preserve channel and exact integer sample position.  Reader offset
changes were prohibited.

The experiment therefore used only the explicitly frozen equal-capacity
representation reversal.  Because the current labels are second-order
relations over transition signs, endpoint exchange and sign negation cancel;
the correct mapping is:

`(r0, r1, r2) -> (r2, r1, r0)`

with `same-zero`, `same-active`, `up`, and `down` unchanged.  No raw-waveform
reverse claim is made.

## Interpretation

The result sharpens the representation bottleneck:

- global directional counts and their relative changes transfer across these
  sources, but did not prefer the forward direction over controls;
- retaining the complete three-step same-anchor linkage restores information
  removed by pooling, but the resulting histogram has no cross-source
  recurrence at all;
- the present family therefore sits between an overly exchangeable
  representation that loses direction and an overly specific representation
  that loses transfer.

This is bounded evidence from two reusable development sources.  It does not
prove that all local relational or audio learning is impossible.  It does show
that tuning trajectory length, selecting path bins, weakening exact matching,
or adding a gate on this pair would be post-result model selection and is not
authorized.

## Binding decision

- Keep v1.43 isolated and inactive.
- Do not rerun this frozen attempt.
- Do not tune or enumerate further anchor/count trajectory variants on these
  two development archives.
- Do not modify or activate the provisional reader.
- Do not proceed to another external validation.
- Do not reread the original MP4 files, the old eleven sources, or the failed
  external-validation group.

The current line stops at the unresolved requirement for a representation that
is simultaneously source-transferable and direction-bearing.

## Files

- `A_ANN_ANCHOR_TRAJECTORY_CANDIDATE_FREEZE_20260829.md`
- `ann_anchor_trajectory_temporal_v1_43.py`
- `test_ann_anchor_trajectory_temporal_v1_43.py`
- `run_ann_anchor_trajectory_development_ab_20260829.py`
- `ann_anchor_trajectory_development_ab_20260829_attempt.json`
- `ann_anchor_trajectory_development_ab_20260829_report.json`

Pre-run targeted tests and the complete local regression passed: 239/239.  A
post-run static audit then reverified every frozen hash, control capacity,
admission count, and decision invariant; the complete regression again passed
239/239 without rereading either archive.  Neither original MP4 was decoded or
read during this experiment.

