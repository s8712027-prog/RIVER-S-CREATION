# ANN/A anchor-trajectory candidate freeze — 2026-08-29

## Status and purpose

This document freezes one development-only candidate before either reusable
development archive is evaluated.  The active reader remains unchanged and
provisional.  This candidate is not authorized for activation or external
validation merely because it has been implemented.

The concrete reason for the candidate is the located loss at global count
aggregation.  Three directional-position states currently become three
independent four-label count vectors.  That operation discards whether the
same sensor anchor continued through a particular ordered relation path.

The candidate therefore performs exactly one new operation:

> link the three observations belonging to each fixed anchor before pooling,
> then pool the eight resulting trajectories without retaining anchor identity.

## Frozen representation

- Input remains the existing 100 ms PCM windows and existing eight anchors.
- No reader offset, traversal rule, threshold, sign rule, relation label, or
  archive format changes.
- Each admitted occurrence consists of three adjacent existing
  `directional_position_topology` states.
- For anchor `a`, form the ordered trajectory
  `(relation[a,t], relation[a,t+1], relation[a,t+2])`.
- Pool only after linking: count the multiset of the eight trajectories over
  the fixed 64 possible three-label paths.
- The key contains no source hash, anchor index, channel identity, or selected
  path list.  Matching is exact equality of the complete sparse histogram.
- Preserve the three existing full-motif evidence tokens.  Their overlapping
  union spans five raw PCM windows.
- Retain the existing temporal admission rule exactly: every state must contain
  at least two relation categories, and the three global count states must be
  neither constant nor forward/reverse symmetric.  Add no candidate-specific
  admission gate, including no gate that removes reverse-compatible trajectory
  histograms.

## Reverse-control boundary

The current alternating stereo anchor geometry is not exactly closed under
raw-waveform time reversal: mirroring an offset must preserve its channel, but
the existing mirrored anchor generally lies in the other channel, and integer
offset rounding can also miss by one sample.  Changing that geometry would
violate the current-line prohibition on reader offset changes.

Accordingly, the frozen reverse control is explicitly an equal-capacity
**representation reversal**, not a raw-waveform reversal.  The four relation
labels remain unchanged under reversal because they are second-order relations
over transition signs: endpoint exchange and sign negation cancel.  Each path
is therefore mapped only as

`(r0, r1, r2) -> (r2, r1, r0)`.

Every admitted held-out occurrence produces exactly one reversed occurrence.
No raw-reversal claim may be made from this experiment.

## Frozen controls

The formation archive is `ann_development_233248_neutral_archive_v0_1.npz` and
the held-out archive is `ann_development_233446_neutral_archive_v0_1.npz`, as
already fixed by acquisition order.  Each is read for 64 shared-reader turns
using fresh existing ledgers.  The original MP4 files are not read or decoded.

Controls are built before trajectory pooling and use the same complete
histogram and exact-matching rule:

1. Representation reversal: reverse all three-step held-out paths.
2. Other time orders: use each of the four non-forward, non-reverse
   permutations of the same three states.
3. Anchor-link break: keep the first state fixed and cyclically permute the
   later two states within each channel.  Enumerate all fixed shift pairs that
   break both adjacent same-anchor links.  This preserves every time-local and
   channel-local label marginal.
4. Time-adjacency break: use cyclic bijections over the complete constructible
   held-out base occurrences for each fixed positive shift up to 31.  State 0, state 1,
   and state 2 each use every original positional marginal exactly once per
   trial.  Admit a shift only when every synthetic trajectory uses three
   distinct base occurrences and its two coordinate links are neither the
   original forward nor reverse adjacency.  The valid-shift rule uses only
   frozen coordinates, never relation labels or match outcomes.

Forward and every transformed control start from exactly the same complete set
of constructible held-out base coordinates.  The same existing admission rule
is applied independently after each transformation.  Reports must state both
attempted and admitted occurrence counts.  Reverse and anchor-link transforms
are expected to preserve admission mathematically; other-order and time-spliced
controls may have different admitted counts because the unchanged temporal
admission rule is itself order-sensitive.  No control may be formed only from
the forward-admitted subset.

No control is selected after seeing its result.  The maximum count across all
predeclared controls is the comparison boundary.

## Frozen decision rule

Pass only if all conditions hold:

- at least one formation structure is supported in held-out data;
- forward supported-structure count is strictly greater than representation
  reversal and every individual broken-order, broken-link, and
  broken-time-adjacency control;
- every forward match has disjoint exact evidence across the split;
- forward support exceeds the exact-count baseline support of zero.

A tie is a Fail.  Zero support is a Fail.  A control that exceeds forward is a
Fail.  Inconclusive is reserved for inability to construct the frozen
candidate or equal-capacity controls because of missing/incompatible archive
structure; it is not used for an unfavorable result.

The run is single-shot.  After a Fail, do not change trajectory length,
histogram bins, permutations, admission, matching, or read budget on these two
archives.  Stop the present anchor/count representation family and return to
the research boundary.

Before the first archive load, the runner must create an exclusive attempt
marker.  The marker remains even if execution terminates unexpectedly, so an
exception cannot silently authorize another look at the same frozen candidate.

