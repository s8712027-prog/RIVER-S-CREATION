# ANN/A current-line handoff — post external validation fail v4

## Authority and exact current state

This file supersedes
`A_CURRENT_LINE_HANDOFF_DYNAMIC_LOCAL_READING_V3.md` for continuation status.
The v3 invariants and prohibitions remain binding except that the awaited
external validation has now occurred.

The frozen local-capability reader completed one external validation on three
previously untouched MP4 sources supplied on 2026-08-28.  The predeclared
decision was **Fail**, not `Inconclusive`.

The local-capability reader is not promoted beyond `provisional`.  No
post-outcome tuning, new gate, or protocol was added.  The three external
sources are no longer untouched and must never be presented as a fresh
external-validation group.

## What was executed

- Source order and split were frozen before outcome inspection.
- The first two sources formed candidates; the third remained isolated
  heldout.
- Each source was decoded exactly once into neutral RGB/PCM/shared-timestamp
  form.
- The active categorical local-capability policy received 64 shared reads per
  source.
- Reversed-order and all eligible deterministic adjacency-broken controls were
  evaluated from the resulting ledgers.
- The old eleven sources and their archives were not read or rerun.
- No parameter or representation was changed after the result.

Primary result files:

- `ann_external_validation_20260828_freeze_manifest.json`
- `ann_external_validation_20260828_decode_report.json`
- `ann_frozen_external_validation_20260828_report.json`
- `A_ANN_FROZEN_EXTERNAL_VALIDATION_20260828.md`

## Exact external result

Audio:

- 97 formation temporal structures and 55 heldout temporal structures;
- 2 formation-to-heldout supported structures;
- 2/2 supported structures retained distinct exact evidence;
- reversed-order match count 1;
- 31 adjacency-broken trials, mean 0.742 and maximum 3;
- observed 2 did not exceed the adjacency-broken maximum 3;
- empirical null upper p-value 0.1875;
- result: Fail.

Visual:

- 40 formation temporal structures and 18 heldout temporal structures;
- 0 formation-to-heldout supported structures;
- 19 eligible adjacency-broken trials, all with 0 matches;
- observed 0 did not strictly exceed the controls;
- result: Fail.

## Failure localization

The evidence does not identify ingestion failure:

- all three sources supplied hundreds of RGB frames;
- all three supplied 16 kHz stereo PCM after neutral transduction;
- both modalities had eligible adjacency-broken trials.

The evidence also does not identify reader inactivity as the primary failure:

- the three sources completed all 64 authorized reads;
- their maximum start windows were 68, 70, and 67;
- adjacent triple counts were 54, 49, and 55;
- the local policy generated +2 actions on every source.

The observed bottleneck is cross-source stability of the learned
representation:

- the two formation sources produced many within-source structures but zero
  audio and zero visual structures shared across both formation sources;
- the two audio heldout matches did not exceed adjacency-broken structure
  collisions;
- no visual structure reproduced across the split.

This is an evidence-based localization, not proof that the reader policy can
never contribute to the failure.  It does mean that modifying reader traversal
first is not justified by this result alone.

## Binding continuation prohibitions

- Do not rerun or re-decode the three 2026-08-28 external sources.
- Do not tune thresholds, topology, offsets, controls, or gates against their
  result.
- Do not reread, re-decode, or rerun the old eleven development sources.
- Do not reinterpret the two audio matches as generalization; they failed the
  maximum adjacency-broken control.
- Do not dismiss the result as insufficient material; the frozen
  `Inconclusive` conditions were not met.
- Do not next expand CRC, relationship persistence, first-person persistence,
  ingestion rules, or coordinator modules.
- Do not delete, move, rename, or otherwise manage the user's original videos
  or derived neutral archives.

## Next meaningful development boundary

No immediate code change is authorized by the failed group itself.  If the
mainline is to resume algorithm development, it requires a **separate group
explicitly designated as reusable development material**.  It cannot be any of
the old eleven sources or the three failed external-validation sources.

That development phase should investigate representation invariance rather
than adding a decision gate:

1. preserve neutral RGB/PCM/shared timestamps and exact evidence;
2. preserve the categorical local reader as the comparison baseline;
3. ask why ordered directional-count triples are abundant within sources but
   unstable across sources;
4. compare any replacement representation on the separate development group;
5. do not claim external improvement from development material;
6. after freezing a justified replacement, require another genuinely untouched
   group for one external validation.

At least two distinct audiovisual development sources are required to observe
cross-source stability at all.  More diversity may improve diagnosis, but a
larger count by itself is not evidence of learning.

Until separately designated development material exists, report:

> The frozen reader failed external validation at the cross-source
> representation-stability boundary.  The result is sealed; further tuning on
> the validation sources is prohibited.

Then stop.  Do not create substitute implementation work.

## Invariants that remain binding

- A begins from unknown state; `who`, `from`, `where`, and `have` remain
  unresolved first-person learning drives.
- Passive audiovisual evidence cannot be converted into invented self answers.
- Event learning and relationship judgment remain decoupled:
  `learning ⟂ relation`.
- Formation, revision, challenge, withdrawal, and replacement remain
  append-only.
- Relationship top-level paths and generation-qualified SLOT identity rules
  remain unchanged.
- CRC remains read-only and cannot create or adjudicate learning candidates.
- The parallel model line remains separate and may exchange only methods,
  formats, and test results.

