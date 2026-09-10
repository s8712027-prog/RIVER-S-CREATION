# ANN/A local ordinal-moment branch charter v2

## Status and isolation

This charter supersedes the audited no-go ordinal-flux v1 proposal.  It freezes
the mathematical family for synthetic-only implementation before any new
source is read.  The provisional reader remains unchanged; existing
development, old, and failed-external materials remain forbidden.

The v1 pair-current endpoint was rejected before implementation because it was
a disguised low-cardinality global count.  The v2 endpoint is a pair of parity
moments over a tie-safe ordinal rank profile.  It neither pools category counts
nor retains the full ordered trajectory.

## Observation primitive

For every channel of one complete 100 ms PCM window:

1. Require an exact `N = 8q` frame count and partition the channel into eight
   equal contiguous, mirror-closed microbins.
2. Sort each microbin and compute a doubled median from its two central
   operands, promoted to widened arithmetic before addition.  For odd `q` the
   central operand is added to itself.  All PCM values must be finite.  The
   future neutral real-data domain is exactly `float32`; signed integer PCM of
   at most 32 bits is accepted only for safe synthetic fixtures.  Unsigned,
   64-bit integer, and `float64` inputs are rejected rather than silently
   changing the arithmetic contract.
3. From the eight doubled medians `M[0..7]`, form seven local roughness
   magnitudes:

   `e[j] = abs(M[j+1] - M[j])`, for `j = 0..6`.

Microbin medians use the bin's complete sample multiset.  No point anchor,
threshold, epsilon, FFT, semantic label, source label, or learned normalization
is present.

## Tie-safe ordinal profile

For each `e[j]`, define the integer ordinal score:

`r[j] = sum(sign(e[j] - e[k]) for every k != j)`.

This equals `2 * midrank(e[j]) - 6` for seven values, handles ties without a
threshold, and always satisfies `sum(r) = 0`.

Let `x[j] = j - 3`.  Define exactly two integer moments:

- reversal-even carrier:
  `C = sum((x[j]^2 - 4) * r[j])`;
- reversal-odd arrow:
  `F = sum(x[j] * r[j])`.

The occurrence key is the exact ordered pair `(C, F)`.  `F = 0` occurrences
remain in all capacity and diversity reports but cannot count as oriented
support.  No `C -> sign(F)` predictor, magnitude bin, partial moment, or fallback
key is allowed on the same materials.

## Exact symmetries

Raw frame-axis reversal is performed inside each channel, never over flattened
interleaved samples.  It maps:

- `M[j] -> M[7-j]`;
- `e[j] -> e[6-j]`;
- `r[j] -> r[6-j]`;
- `(C, F) -> (C, -F)`.

Mathematically, the key is invariant to each channel's independent affine
transform `x -> a*x + b` for any nonzero `a`, provided the transform itself is
exact and does not clip or requantize.  This includes DC shift, positive gain,
and microphone polarity flip; channel permutation and duplicated-channel
scaling preserve source incidence.  In the implementation, `float64` exactly
represents every accepted `float32` operand, but a central-pair sum with a very
large exponent gap can still round in `float64`.  Reversal and polarity reuse
the same widened operands up to exchange or sign, so their key identities
remain exact under the same finite IEEE operations and are not tolerance
claims.  All doubled medians, differences, and absolute differences from
accepted signed <=32-bit synthetic integers are exact.  The implementation
does not claim that an arbitrary affine transform followed by `float32`
requantization must preserve a key.

For strict ranks, the complete seven-value order has 5,040 permutations.  The
two frozen moments yield 1,735 keys, of which 1,692 have `F != 0`; median key
preimage is 3 and maximum is 13.  This establishes a concrete compression
between global counts and complete trajectory identity before source data.

## Synthetic-only gates

An isolated implementation may proceed without any archive I/O.  It must prove:

- all `7!` strict rank permutations reproduce the frozen 1,735-key census,
  median preimage 3, and maximum preimage 13;
- all 47,293 seven-position weak orders, including every tie structure,
  satisfy `(C,F)_reverse = (C,-F)`;
- raw synthetic PCM reversal recomputes the exact transformed key;
- applying reversal twice restores every key and evidence coordinate;
- positive/negative gain and DC shift preserve keys for safe finite synthetic
  samples;
- channel permutation and duplication preserve per-source distinct-key
  incidence;
- microbin-internal sample permutations preserve keys;
- every adjacency and carrier-arrow linkage control preserves attempted
  capacity and its declared marginals;
- zero or one-key support, forward/reverse ties or reverse excess, and control
  ties or excess all fail.

The public synthetic evaluator accepts only three raw formation segments and
three raw held-out segments.  It derives the raw reversals, all 28 adjacency
controls, all 31 linkage shifts, occurrence capacities, PCM invariants, and
exact-evidence checks internally.  Caller-supplied reverse keys, partial
control mappings, or default-true audit flags are not an allowed interface.
The decision record also reports per-source occurrence capacity, distinct-key
count, `F=0` occurrence count, and stricter 3-of-3 formation and held-out
incidence.

No neutral archive or original media may be opened during this phase.

## Required new materials

Real-data development is not yet authorized.  It requires six wholly new,
independent recordings, each with at least 6.4 seconds of compatible audio
after one neutral decode.  Roles are frozen by acquisition order before any
decode or feature read:

- F1–F3: formation;
- H1–H3: held-out development.

At least three additional independent recordings X1–X3 must be named and
sealed as external validation.  They are not decoded or feature-read unless
development passes.  All nine sources must be new to model design.  The current
233248/233446 pair, old eleven, and failed external group are excluded.

The fixed observation budget is the first 64 complete contiguous 100 ms
windows per source.  Sample rate, channel layout, finite PCM, and exact
eight-way window divisibility must be compatible.  A role manifest and
single-shot marker containing spec, implementation, control, and source-role
hashes must exist before F1 is loaded.

## Formation and support

Each source contributes a set of distinct `(C,F)` keys from its fixed windows
and channels; repeated occurrences within one source do not inflate support.

The frozen formation dictionary is:

`A = {key | F != 0 and key occurs in at least 2 of F1,F2,F3}`.

For held-out source `Hh`, let `s_h` be the number of distinct keys in `A` that
occur in that source.  Overall forward support `S` is the number of distinct
keys in `A` occurring in at least 2 of H1,H2,H3.

Every supported key must retain source-disjoint exact window evidence in at
least two formation and two held-out sources.  Report the stricter 3-of-3
formation and held-out incidence separately, but do not use it as an alternate
decision path.

## Equal-capacity controls

All controls use the identical held-out source windows and channels.

1. **Raw reversal.** Reverse PCM frames per channel and recompute the full
   primitive.  Assert occurrence-by-occurrence `(C,F) -> (C,-F)`.  Compute
   aggregate reverse support and each `s_h_reverse`.
2. **Adjacency break.** For each occurrence's `e[0..6]`, independently apply
   all 28 fixed affine permutations
   `p(j) = (a*j + b) mod 7`, with `a in {2,3,4,5}` and `b in 0..6`.  Every
   permutation preserves the exact `e` multiset and contains no original
   forward or reverse neighboring edge.  Recompute ranks and moments and score
   every control individually.
3. **Carrier-arrow linkage break.** Within each held-out source's frozen
   occurrence order—window-major, then channel-minor—retain `C[i]` and pair it
   with `F[(i+s) mod n]` for every fixed shift `s = 1..min(31,n-1)`.  This
   preserves exact C and F marginals and occurrence capacity while destroying
   same-occurrence linkage.  Score every shift individually.
4. **Invariant audits.** PCM polarity inversion and channel permutation must
   leave keys unchanged.  These are mandatory invariants, not null competitors.

Formation remains forward and frozen.  No control is selected, averaged, or
filtered after match results are known.

## Decision boundary

Pass only if all conditions hold:

- `S >= 2` distinct oriented keys;
- `S` is strictly greater than aggregate raw-reverse support and every
  individual adjacency and linkage control;
- every held-out source satisfies `s_h > s_h_reverse`;
- every supported key has the required source-disjoint exact evidence;
- all attempted capacities, raw-reversal identities, source roles, hashes, and
  invariants pass.

Any formation insufficiency, `S < 2`, held-out `s_h <= s_h_reverse`, aggregate
reverse support greater than or equal to `S`, any individual control score
greater than or equal to `S`, exact-evidence collision, or failed mandatory
capacity/identity/role/hash/invariant is a Fail.  Positive reverse support
below forward is reported but is not by itself a failure.

Inconclusive is reserved only for frozen I/O or structural incompatibility that
prevents equal-capacity construction.  It is never a label for unfavorable
evidence.

The development run is single-shot.  After result, do not tune microbin count,
window count, statistic, ranks, moments, key, source-incidence threshold,
controls, split, or fallback prediction on those sources.

## Current stopping point

This charter authorizes only a synthetic-only reference implementation and
property tests.  Stop before real-data code execution until F1–F3, H1–H3, and
sealed X1–X3 are supplied and role-designated.

