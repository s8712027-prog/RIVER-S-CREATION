# ANN/A current-line handoff — representation development v5

## Authority

This file supersedes
`A_CURRENT_LINE_HANDOFF_POST_EXTERNAL_FAIL_V4.md` for continuation status.
All first-person, append-only, relationship, SLOT, CRC, parallel-line, compute,
and local-file boundaries from v4 remain binding.

## Exact current status

The three-source frozen external validation failed.  After that result, two
separate MP4 sources were explicitly designated reusable development material
and decoded once into neutral archives.

The current exact-count representation was re-established as a development
baseline.  Two minimal representation replacements were then tested and both
were rejected by predeclared controls.  No candidate was activated; the
local-capability reader and active mainline files remain unchanged.

## Development evidence

Current exact directional-count triple:

- supported audio structures 0;
- reversed 2;
- adjacency-broken maximum 3.

Ordinal directional-count triple:

- supported audio structures 1;
- reversed 3;
- adjacency-broken maximum 4;
- rejected as collision-producing coarsening.

Signed directional-count changes:

- supported audio structures 10, all with distinct exact evidence;
- correctly inverted true reverse 12;
- adjacency-broken maximum 11;
- empirical null upper p-value 0.0625;
- rejected despite substantial cross-source improvement.

The most informative result is the signed-change candidate: relative count
dynamics transfer across sources much better than absolute count states, but
the transferred structures are not yet preferentially forward in time.

## Binding decision

- Do not activate v1.40 or v1.41.
- Do not tune a threshold, exclude reverse-matching patterns, or add an
  admission gate to force v1.41 to pass.
- Do not modify the local-capability reader first; it completed the bounded
  traversal and is not the located bottleneck.
- Do not use the failed external three-source group for development.
- Do not read or rerun the old eleven sources.
- The two `233248` and `233446` neutral archives are reusable development
  material but are permanently ineligible as untouched validation.
- Do not claim external generalization from any result in this development
  phase.

## Next unresolved mainline question

The next representation must answer one precise question:

> How can ANN retain the cross-source stability of relative count changes while
> retaining enough forward temporal orientation to exceed a correctly inverted
> reverse control and adjacency-broken controls?

Do not answer this by trying many token variants on the same turn.  Before a
new implementation, derive a representation-level reason for forward
orientation that comes from the ordered evidence itself, not from a learned
threshold, scene label, source identity, or evaluator gate.

Additional reusable development material may later test whether the 10-versus-
12 result was pair-specific, but a larger source count alone is not a fix and
does not authorize promotion.  Another untouched external group is required
only after a development candidate is justified, frozen, and clears its
development controls.

## Primary files

- `A_ANN_REPRESENTATION_DEVELOPMENT_20260828.md`
- `ann_representation_development_baseline_20260828_report.json`
- `ann_ordinal_directional_count_development_ab_20260828_report.json`
- `ann_directional_count_delta_development_ab_20260828_report.json`
- `ann_ordinal_directional_count_temporal_v1_40.py` — rejected development
  artifact, inactive.
- `ann_directional_count_delta_temporal_v1_41.py` — rejected development
  artifact, inactive.
- `ann_shared_timeline_av_reader_v1_21.py` — unchanged active provisional
  reader.

Until a reasoned forward-oriented representation is proposed, report:

> Relative count changes improved development cross-source support from 0 to
> 10 but failed true reverse and adjacency controls.  Both tested replacements
> remain inactive; the mainline is stopped at the forward-orientation
> representation boundary.

Then stop.  Do not create substitute modules or protocols.

