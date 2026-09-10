# ANN/A forward prediction development — 2026-08-28

## Question

Could relative directional-count changes acquire a forward time orientation
when they are learned as append-only context-to-successor predictions rather
than compared only as complete matching structures?

## Candidate

- Four adjacent exact PCM motifs supply three relative count-change states.
- The first two ordered changes form a context.
- The third change is the successor to be predicted.
- Every observed edge is retained append-only; ambiguous contexts are not
  deleted or hidden.
- A categorical prediction exists only when one observed formation context has
  exactly one recorded successor.  This is an exact property, not a fitted
  numeric threshold.
- Forward and reverse learners have equal context length and capacity.
- Reverse evidence reverses the change order and inverts every `up/down`
  direction.
- Adjacency-broken controls preserve observed context and target marginals.

Before execution, an invalid comparison was rejected: complete edge matches
cannot reveal time direction because forward and reversed edges are related by
a bijection.  The executed comparison therefore measured unique-successor
constraint, where forward and reverse conditional branching can differ.

## Development result

Both reusable development archives received the same fixed 64-read policy.
They produced 61 formation and 55 heldout prediction examples.

Formation model:

- 41 distinct contexts;
- 29 contexts with exactly one successor;
- 12 ambiguous contexts;
- at most 3 successors for one context;
- 61 append-only prediction revisions.

Forward heldout result:

- 2 correct distinct deterministic predictions;
- 12 incorrect distinct deterministic predictions;
- 2/2 correct predictions retained exact evidence distinct from formation.

Equal-capacity reverse result:

- 3 correct distinct deterministic predictions;
- 13 incorrect distinct deterministic predictions;
- 3/3 correct predictions retained distinct exact evidence.

Adjacency-broken result:

- 31 eligible trials;
- mean correct predictions 0.774;
- maximum correct predictions 3;
- empirical null upper p-value 0.28125.

Decision: **reject development prediction candidate**.  Forward 2 did not
exceed reverse 3 or adjacency-broken maximum 3.

## Interpretation

Changing the learning question from structure equality to categorical
prediction did not recover a time arrow.  The relative-count representation
appears to lose direction-bearing information before the prediction layer sees
it.  A downstream predictor cannot reconstruct information removed by global
count aggregation.

This result does not justify:

- selecting only the two successful forward patterns;
- excluding contexts that also work in reverse;
- changing context length until one variant passes;
- adding a confidence threshold;
- modifying reader offsets;
- claiming external generalization.

## Verification boundary

- 18 targeted prediction, delta, and shared-reader tests passed.
- The active reader was not modified.
- Original MP4 files were not re-decoded.
- Old development and failed external-validation sources were not read.
- The prediction module remains an isolated rejected development artifact.

Primary files:

- `ann_directional_count_prediction_v1_42.py`
- `test_ann_directional_count_prediction_v1_42.py`
- `run_ann_directional_count_prediction_development_20260828.py`
- `ann_directional_count_prediction_development_20260828_report.json`

