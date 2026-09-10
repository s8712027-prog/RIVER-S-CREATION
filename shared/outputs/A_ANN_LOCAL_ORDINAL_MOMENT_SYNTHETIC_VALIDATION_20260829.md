# ANN/A local ordinal-moment synthetic validation — 2026-08-29

## Outcome

The isolated local ordinal-moment v2 branch has cleared its synthetic-only
implementation gate.  This means its reversal algebra, tie behavior, frozen
controls, evidence checks, and fail-closed decision path are executable and
internally consistent.  It does **not** show that the representation transfers
between genuinely independent real recordings, and it does not activate or
replace the provisional local-capability reader.

No archive, original video, old source, failed external source, or previously
provided recording was opened, decoded, or feature-read in this phase.

## Design path

The first proposed ordinal-flux endpoint was rejected before implementation.
Exhaustive symbolic analysis showed that its three currents collapse to a
low-cardinality global count.  The retained v2 hypothesis instead compresses a
seven-position tie-safe ordinal roughness profile into two parity moments:

- reversal-even carrier `C`;
- reversal-odd arrow `F`;
- exact occurrence key `(C,F)`, with raw reversal `(C,F) -> (C,-F)`.

The representation neither pools old anchor categories nor preserves a full
trajectory.  It is defined in
`A_ANN_LOCAL_ORDINAL_MOMENT_BRANCH_CHARTER_V2.md`.

## Fail-closed reference boundary

The only frozen evaluation entry point is `evaluate_frozen_segments`.  It
accepts exactly three raw formation segments and three raw held-out segments.
It internally constructs and verifies:

- one raw frame-axis reversal for each held-out source;
- all 28 frozen adjacency-breaking controls;
- all 31 frozen carrier-arrow linkage shifts;
- the complete 64-window-by-channel occurrence grid;
- occurrence-level raw reversal identity;
- PCM polarity and channel-permutation invariants;
- source-disjoint exact channel-window evidence for every supported key.

The prior fail-open surface is gone: callers cannot provide reverse key sets,
partial control mappings, or default-true evidence/invariant flags.  Structural
input inability raises an error for the future runner to classify as
Inconclusive; unfavorable scores and failed mandatory identities cannot be
relabelled Inconclusive by this evaluator.

The earlier module-level occurrence decision helper was removed.  The raw 3+3
segment function is the sole decision entry point, canonicalizes occurrence
order as window-major then channel-minor, and rejects rebinding of the frozen
64-window, 31-linkage, moment-weight, or 28-order manifest.  Its decision
record includes source capacities, distinct-key counts, `F=0` counts, and the
stricter 3-of-3 incidence sets.

Accepted PCM is finite neutral `float32`, or signed integer PCM of at most 32
bits for safe synthetic fixtures.  `float64`, unsigned integers, and 64-bit
integers are rejected.  A signed synthetic integer segment whose minimum value
cannot be polarity-inverted in the same dtype is also rejected structurally.

## Exhaustive symbolic results

| Audit | Frozen result |
|---|---:|
| Strict seven-rank permutations | 5,040 |
| Distinct `(C,F)` keys | 1,735 |
| Keys with `F != 0` | 1,692 |
| Median strict-key preimage | 3 |
| Maximum strict-key preimage | 13 |
| Complete seven-position weak orders checked | 47,293 |
| Frozen adjacency controls | 28 |
| Frozen linkage controls | 31 |

Every weak order, including every tie structure, satisfied exact reversal.
All 28 adjacency orders were distinct full permutations with no original
forward or reverse neighboring edge.  Every linkage shift preserved occurrence
capacity and exact carrier/arrow marginals.

## Synthetic decision fixtures

The positive fixture deliberately used six byte-distinct affine transforms of
one seeded two-channel synthetic PCM segment.  It is an invariance oracle, not
a simulation of six independent sources and not evidence of real transfer.

| Quantity | Result |
|---|---:|
| Formation dictionary | 123 keys |
| Forward support | 123 keys |
| Aggregate raw-reverse support | 14 keys |
| Per-held-out forward | 123 / 123 / 123 |
| Per-held-out reverse | 14 / 14 / 14 |
| Individual controls attempted | 59 |
| Maximum individual control support | 18 keys |
| Raw reversal identity | pass |
| PCM invariants | pass |
| Exact evidence disjointness | pass |
| Synthetic decision | retain development candidate |

Two mandatory negative fixtures also behaved correctly:

- six identical raw segments failed exact-evidence disjointness and were
  rejected;
- a source family containing only one recurrent oriented key was rejected
  because the frozen minimum is two.

## Tests and read-only verification

- Targeted v2 tests: 19/19 passed.
- Complete local regression: 258/258 passed.
- The full discovery covered 45 `test_ann_*.py` files.
- A separate read-only runner audit found no archive/media path or load literal
  in that test execution and confirmed that `evaluate_source_incidence` is no
  longer present and that no module-level occurrence decision helper remains.
- Independent mathematical and fail-open red-team audits both approved closure
  of the synthetic-only phase.  Their approval does not open the real-data
  gate.

Frozen SHA-256 values at validation:

- implementation `ann_local_ordinal_moment_v2_0.py`:
  `F08C1CB633941F5C3640638464CD4C7BD352E1D42382E4845C6A3746E38A9857`;
- tests `test_ann_local_ordinal_moment_v2_0.py`:
  `0EFB05A7CB50E7498477A4993C7AFA1353FFB1319689E9DFFCFD5F46A6A5E580`;
- charter `A_ANN_LOCAL_ORDINAL_MOMENT_BRANCH_CHARTER_V2.md`:
  `58C94D46732C5A2751A6B6797EAC17C446EE18AF3DC7BE9041D3F911F3B6F095`.

## Claim boundary and next gate

The synthetic phase supports exactly one next step: acquire and role-freeze
nine wholly new recordings using
`A_ANN_LOCAL_ORDINAL_MOMENT_NEW_MATERIAL_ROLE_MANIFEST_TEMPLATE_V2.md`.
F1–F3 and H1–H3 are development; X1–X3 remain sealed external validation.

Four user-supplied paths have since been registered, without file access, as
F1, F2, F3, and H1 in
`A_ANN_LOCAL_ORDINAL_MOMENT_NEW_MATERIAL_ROLE_MANIFEST_V2_20260829.md`.
H2, H3, X1, X2, and X3 remain missing.

Until all nine new sources are supplied and frozen, do not build a real-media
runner, decode any source, tune v2, reuse earlier material, run external
validation, or modify the active reader.

