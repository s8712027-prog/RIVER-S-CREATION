# ANN/A current-line handoff — forward prediction fail v6

## Authority

This file supersedes
`A_CURRENT_LINE_HANDOFF_REPRESENTATION_DEVELOPMENT_V5.md` for continuation
status.  All prohibitions and model invariants from v5 remain binding.

## Current state

The active mainline remains unchanged and provisional.  The external
validation failed.  On the separate reusable development pair, exact counts,
ordinal counts, signed count changes, and now categorical forward prediction
have all failed their controls.  None is authorized for activation.

The new prediction candidate used two relative changes as an ordered context
and predicted the third.  It retained every observation append-only and gave
the reverse learner identical capacity with correctly inverted temporal
direction.

Result:

- forward correct deterministic predictions: 2;
- equal-capacity reverse correct predictions: 3;
- adjacency-broken maximum: 3;
- all 2 forward successes had distinct exact evidence;
- decision: reject.

## Updated failure localization

The failure is no longer adequately described as only a matching-policy
problem.  Relative count changes improved cross-source recurrence, but both
direct structure comparison and conditional prediction failed to prefer the
forward direction.

The located information loss occurs at or before global count aggregation:

- fixed anchor directions are collapsed into four global counts;
- relative changes of those counts transfer across sources;
- however, forward and backward conditional constraints remain comparable;
- a downstream prediction ledger cannot reconstruct temporal orientation that
  the count representation discarded.

This is an inference from the bounded development evidence, not proof that
every count-based model is impossible.

## Binding decision

- Keep v1.40, v1.41, and v1.42 inactive.
- Do not alter prediction context length, filter patterns, or tune confidence
  on the reusable development pair merely to obtain a pass.
- Do not add a new gate that rejects reverse-compatible evidence.
- Do not modify local reader offsets; reader traversal remains outside the
  located failure.
- Do not reactivate old whole-dataset work or the failed external group.
- Do not expand CRC, relationship, first-person persistence, coordinator, or
  ingestion protocols.
- Do not claim language, semantic, object, causal, or self learning.

## Next unresolved research boundary

Before another implementation, identify a neutral direction-bearing property
that survives across sources but is lost by global count aggregation.  It must
come from the ordered sensor evidence itself and remain available to both
forward and reverse controls.

Potentially relevant evidence classes may include within-window order or
limited anchor-position relations, but this statement is not authorization to
activate the earlier position-specific representation or enumerate variants.
A new candidate requires a concrete reason that it can retain direction
without returning to source-specific exact patterns.

More development sources may determine whether the present result is
pair-specific, but source count alone does not solve the representation
problem.  No new external validation should occur until one development
candidate is justified, frozen, and clears forward, reverse, and
adjacency-broken controls.

## Current report

`A_ANN_FORWARD_PREDICTION_DEVELOPMENT_20260828.md`

Until a new direction-bearing representation is justified, report:

> Categorical prediction over relative count changes produced 2 forward
> successes, versus 3 reverse and an adjacency-broken maximum of 3.  The
> candidate is rejected.  The mainline is stopped at direction-bearing sensor
> representation before global count aggregation.

Then stop.  Do not create substitute implementation work.

