# ANN/A current-line handoff — anchor trajectory fail v7

## Authority

This file supersedes
`A_CURRENT_LINE_HANDOFF_FORWARD_PREDICTION_FAIL_V6.md` for continuation status.
All earlier prohibitions and active-model invariants remain binding unless this
file explicitly narrows them further.

## Current model state

The active mainline remains unchanged and provisional.  The local-capability
reader is still the provisional default; its SHA-256 remains:

`74AAA1AF2AACAD0FF8B13DF5DD9D472CBE91F95D07C87F9F773352FF0DD81ACA`.

The earlier full regression remained green, and the new isolated candidate plus
the complete local suite passed 239/239 tests before the bounded run.  No v1.43
code is active or allowed to drive reading.

## Newly completed work

One concrete direction-bearing representation was justified and frozen before
data access: link each anchor's three ordered directional relations before
pooling, then match the complete eight-trajectory histogram without anchor,
channel, or source identity.

The only permitted bounded development run has completed on the two already
designated reusable neutral archives, 64 shared-reader turns each:

- formation base/admitted/unique: 62 / 60 / 60;
- held-out base/admitted/unique: 58 / 51 / 51;
- forward supported structures: 0;
- representation reverse: 0;
- four other time orders: all 0;
- nine within-channel anchor-link breaks: all 0;
- thirty valid equal-attempt time-adjacency breaks: all 0;
- control-fairness errors: none;
- decision: reject v1.43.

The single-shot attempt is permanently recorded by
`ann_anchor_trajectory_development_ab_20260829_attempt.json`.  It must not be
rerun.  The original MP4 files were not read or decoded.

A post-run static audit completed after the result: frozen hashes matched the
attempt marker; all controls had the required 58 attempted held-out base
coordinates; reverse and all nine anchor-link controls preserved the 51
admitted occurrences; control-fairness errors remained empty; and the complete
regression passed 239/239 without rereading either neutral archive.

## Updated failure localization

The evidence now locates a transfer-orientation tradeoff inside the current
anchor/count representation family:

- global count and relative-count representations can recur across sources,
  but forward structure does not beat reverse or broken-adjacency controls;
- the complete same-anchor trajectory histogram retains the linkage discarded
  by global pooling, but yields zero cross-source recurrence;
- therefore downstream matching or prediction cannot repair the loss, while
  simply restoring all same-anchor linkage is too source-specific.

This is a bounded inference, not a proof against every relational or audio
representation.

## Reverse-control limitation

The existing alternating stereo anchor geometry is not exactly closed under
raw-waveform time reversal.  A mirrored coordinate must preserve both channel
and sample offset, and none of the eight current coordinates has the required
exact mapping.  Changing offsets is forbidden on this line.

v1.43 therefore used representation reversal only:

`(r0, r1, r2) -> (r2, r1, r0)`.

The four labels remain unchanged because they are second-order relations over
transition signs.  Never describe the completed control as raw-waveform
reversal.

## Binding decisions and prohibitions

- Keep v1.40, v1.41, v1.42, and v1.43 inactive.
- Do not rerun the v1.43 attempt or delete its attempt marker.
- Do not change trajectory length, select trajectory bins, weaken exact
  matching, alter permutations, add admission gates, or tune the 64-read budget
  on the reusable development pair.
- Do not implement pairwise trajectory matrices or another nearby
  anchor/count variant as a substitute continuation on the same data.
- Do not modify local reader traversal or offsets.
- Do not read or decode the two original development MP4s again.
- Do not reactivate the old eleven sources or the failed external-validation
  group.
- Do not expand CRC, relationship, first-person persistence, coordinator,
  ingestion, audiovisual protocol, or semantic/object/causal/self claims.
- Do not run another external validation until a separately justified and
  frozen development candidate first clears its controls.

## Next unresolved research boundary

There is no authorized immediate implementation on the current line.  A valid
continuation requires a genuinely new branch-level hypothesis for a
source-transferable direction-bearing representation, not a parameter variant
of global counts or complete anchor trajectories.

Before code or data, that new branch must state:

1. what invariant should transfer across sources;
2. where temporal orientation remains observable;
3. how exact forward, reverse, linkage-broken, and adjacency-broken controls
   receive comparable capacity;
4. how the representation avoids both global-count information loss and
   source-specific exact trajectory matching;
5. which new materials are development and which remain untouched external
   validation, fixed before any reading.

If genuine raw-waveform reversal is required, a mirror-closed channel-by-time
anchor grid is mathematically necessary.  That changes the fixed observation
protocol and is permitted only as an explicitly authorized new branch, never as
an unannounced modification of the provisional reader.

Until such a branch and new material role are explicitly chosen, report:

> Link-before-pool retained complete three-step same-anchor trajectories but
> produced 0 forward cross-source supports, tied with every frozen control at
> 0.  v1.43 is rejected.  The provisional mainline is unchanged and stopped at
> the source-transferable direction-bearing representation boundary.

Then stop.  Do not create substitute implementation work.

## Current result files

- `A_ANN_ANCHOR_TRAJECTORY_DEVELOPMENT_20260829.md`
- `A_ANN_ANCHOR_TRAJECTORY_CANDIDATE_FREEZE_20260829.md`
- `ann_anchor_trajectory_development_ab_20260829_report.json`
- `ann_anchor_trajectory_development_ab_20260829_attempt.json`

