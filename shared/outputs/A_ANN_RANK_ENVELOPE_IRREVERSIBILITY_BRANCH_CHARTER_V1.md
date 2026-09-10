# ANN/A rank-envelope irreversibility branch charter v1

> **WITHDRAWN BEFORE EXECUTION (2026-08-29).** This draft must not be
> implemented, tested, or treated as a continuation authority.  Its stated
> move away from exact cross-source key recurrence duplicates a direction that
> had already been adopted in the ANN/A mainline.  It was drafted because the
> isolated local ordinal-moment v2 gate incorrectly reintroduced exact `(C,F)`
> recurrence across sources.  That gate does not govern the active provisional
> local-capability reader, which was never reverted.  No media or derived data
> was read for this draft.

## Status and isolation

The user requested continued progress after local ordinal-moment v2 completed a
valid real-data Fail.  This charter authorizes only a new synthetic reference
and mathematical audit.  It does not authorize reuse of the six v2 neutral
derivatives, another decode, modification of the provisional reader, or a new
real-data run.

This is not an ordinal-moment parameter variant.  It abandons exact key
recurrence entirely.  Formation learns one low-dimensional direction of a
third-order time-irreversibility functional; held-out sources are tested for
alignment with that direction.

## Per-occurrence primitive

For each channel of one complete 100 ms PCM window:

1. Require exactly 1,600 finite `float32` samples for the future 16 kHz neutral
   protocol.  Synthetic fixtures may use safe signed integers of at most 32
   bits.
2. Split the channel into ten contiguous, mirror-closed 10 ms bins of 160
   samples each.
3. In each bin, compute doubled median `m2`.  For every sample `x`, compute the
   doubled absolute deviation `abs(2*x-m2)`, then compute its doubled median.
   The resulting ten-value sequence `u[0..9]` is a robust local amplitude
   envelope.  DC shift, gain magnitude, and microphone polarity do not change
   its order in exact arithmetic.
4. Convert `u` to tie-safe ordinal scores
   `q[i] = #values lower than u[i] - #values higher than u[i]`.
   Thus `sum(q)=0`, and reversing the window maps `q[i] -> q[9-i]`.
5. For lags `l in {1,2,3}`, compute the integer lag current

   `J_l = sum(q[i]*q[i+l]*(q[i+l]-q[i]) for i=0..9-l)`.

The occurrence representation is `J=(J1,J2,J3)`.  Raw time reversal maps
`J -> -J` exactly.  It is a third-order weighted irreversibility current, not a
category count, exact trajectory token, roughness moment, selected anchor, FFT,
semantic label, or learned bin.

## Per-source vector and formation template

Each source contributes exactly 64 windows per channel.  Its integer vector is

`V_source = sum(J over all frozen window-channel occurrences)`.

Channel order does not affect `V`; compatible channel duplication only scales
it positively.  No occurrence is admitted, selected, weighted, or discarded.

For formation sources F1–F3, define

`T = V_F1 + V_F2 + V_F3`.

Formation is coherent only if `T != 0` and every source aligns positively with
the other two:

`dot(V_Fi, sum(V_Fj for j != i)) > 0` for all `i`.

For any vector `V`, define the exact scale-bounded alignment

`a(T,V) = dot(T,V) / (L1(T)*L1(V))`,

represented as a reduced rational number.  If either L1 norm is zero, alignment
is exactly zero.  This is not a floating tolerance or fitted threshold.

The forward development score is the exact rational sum

`A_forward = sum(a(T,V_Hh) for h=1..3)`.

Each held-out source must also have strictly positive individual alignment.

## Equal-capacity controls

Formation and `T` remain forward and frozen.  Every held-out control uses the
same 64 windows and channels.

1. **Raw PCM reversal.** Reverse the complete PCM segment per channel and
   recompute the primitive.  Assert occurrence mapping `J -> -J` and source
   vector `V -> -V`.  Score each source and the aggregate with the same
   alignment function.
2. **Ten-bin adjacency break.** For each occurrence apply all 20 fixed orders
   `p(i)=(a*i+b) mod 10`, where `a in {3,7}` and `b in 0..9`, to `q[0..9]`
   before recomputing currents.  Each order preserves the complete q multiset
   and contains no original forward or reverse neighboring edge.  Score all 20
   controls individually.
3. **Cross-half linkage break.** Preserve channel identity.  For each shift
   `s=1..31`, combine `q[0..4]` from window `w` with `q[5..9]` from window
   `(w+s) mod 64` in the same channel.  This preserves exact first-half and
   second-half marginals and all occurrence capacity while breaking their
   within-window linkage.  Score all 31 shifts individually.
4. **Mandatory invariants.** Per-channel PCM polarity inversion and channel
   permutation must preserve every occurrence current up to the corresponding
   channel coordinate.  These are audits, not competing null scores.

The complete frozen competing-control manifest is 51 individual controls plus
raw reversal.  No control may be selected, averaged, omitted, or renamed after
results are known.

## Development decision

Pass only if all conditions hold:

- formation is coherent by all three leave-one-out inequalities;
- every held-out forward alignment is strictly positive;
- every held-out forward alignment strictly exceeds its raw-reverse alignment;
- `A_forward` strictly exceeds aggregate raw reverse and every one of the 51
  individual control aggregate alignments;
- raw reversal, polarity, channel, capacity, hash, role, and exact-evidence
  audits pass.

Any zero vector needed for orientation, nonpositive formation or held-out
alignment, equality, control excess, evidence collision, or failed mandatory
identity is Fail.  Inconclusive is reserved only for structural or I/O inability
to construct the frozen equal-capacity input.  Scores are never Inconclusive.

## Synthetic anti-collapse and property gates

Before any new real material is named or read, the reference must establish:

- exact reversal for all `10! = 3,628,800` strict envelope-rank permutations;
- at least 4,096 distinct `(J1,J2,J3)` vectors over the strict census;
- strict zero-vector prevalence at most 5 percent;
- maximum single-vector prevalence at most 1 percent;
- exact reversal for all `3^10 = 59,049` ternary tied profiles;
- exact raw-PCM reversal, double reversal, safe affine amplitude invariance,
  channel permutation, and within-bin sample permutation;
- uniqueness and declared marginals of all 20 adjacency controls and all 31
  linkage controls;
- a constructed directional fixture passes only when its coherent half-window
  linkage is intact;
- reversible, zero-vector, formation-incoherent, held-out-negative, evidence-
  duplicate, reverse-tie, and control-tie fixtures all fail;
- the public evaluator accepts only raw 3+3 segments and internally constructs
  reversal, all controls, evidence, and invariants.

Failure of any anti-collapse threshold is a pre-data no-go, not an invitation
to change bin count, lags, current formula, or thresholds.

## Future material boundary

Real development remains closed.  If and only if the synthetic gate passes,
a later attempt requires six wholly new development recordings and three new
sealed external recordings, role-frozen before any read.  The six v2 sources,
their neutral derivatives, all earlier sources, and every failed-external
source are excluded.

The real attempt is single-shot.  No tuning, alternate split, fallback key,
or reuse of a failed source is allowed.

