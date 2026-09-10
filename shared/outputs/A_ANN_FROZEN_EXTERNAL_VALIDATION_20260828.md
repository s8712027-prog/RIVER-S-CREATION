# ANN/A frozen external validation — 2026-08-28

## Decision

**Fail under the predeclared external-validation rule.**

This is not `Inconclusive`: all three sources supplied usable RGB and stereo
PCM, and the evaluator obtained 31 eligible audio adjacency-broken trials and
19 eligible visual trials.

The frozen local-capability reader therefore is **not promoted beyond
`provisional`**.  This result does not authorize tuning on these three sources,
adding a new gate, or creating another protocol.

## Frozen procedure

- Source order and split were frozen before outcome inspection: first two
  sources formed candidates; the third remained isolated heldout.
- The active categorical local-capability policy was used with a fixed budget
  of 64 shared reads per source.
- Each MP4 was decoded exactly once into a neutral RGB/PCM/shared-timestamp
  archive.
- The old eleven sources and their archives were not read or rerun.
- Reversed-order and all eligible deterministic adjacency-broken shifts from
  1 through 31 were evaluator-only controls.
- No post-outcome tuning was performed.

## Control result

| Modality | Formation candidates | Heldout observed structures | Supported candidates | Distinct exact evidence | Reversed control | Adjacency-broken max | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Audio | 97 | 55 | 2 | 2/2 | 1 | 3 | Fail |
| Visual | 40 | 18 | 0 | 0/0 | 0 | 0 | Fail |

The two audio matches were not exact-evidence duplicates: both retained exact
evidence disjoint from their formation evidence.  That is a real positive
observation, but it is insufficient because the observed count of 2 did not
exceed the adjacency-broken maximum of 3.  Its empirical null upper p-value
was 0.1875.

The visual representation formed structures within the split but reproduced
none across the split.  Because eligible controls existed, zero observed
support is a failure rather than missing evidence.

## Structure formation and frontier reach

| Source role | Shared reads | Maximum start window | Unread before maximum | Adjacent triples | +1 offsets | +2 offsets |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Formation 231157 | 64 | 68 | 5 | 54 | 59 | 5 |
| Formation 231316 | 64 | 70 | 7 | 49 | 57 | 7 |
| Heldout 231543 | 64 | 67 | 4 | 55 | 60 | 4 |

The reader continued to form many locally adjacent triples and used the +2
action on all three sources.  The failure occurred at cross-source structural
support, not because the reader stopped traversing the timelines.

Across the two formation sources there were 97 distinct active audio temporal
structures and 40 visual temporal structures, but zero structures in either
modality occurred across both formation sources.  On the isolated heldout
source, the reader formed 55 audio and 18 visual temporal structures.

## Interpretation boundary

The evidence supports only the following statement: on this untouched group,
the frozen reader formed substantial within-source temporal structure, but
the audio matches did not beat every adjacency-broken control and visual
structure did not reproduce across the split.  External generalization is not
demonstrated.

The result does not show that no alternative representation could learn from
these sources.  It shows that this frozen representation and reader, under the
fixed 64-read procedure, failed the external criterion.  These three sources
must not be reused as another untouched validation group.

## Evidence files

- `ann_external_validation_20260828_freeze_manifest.json`
- `ann_external_validation_20260828_decode_report.json`
- `ann_frozen_external_validation_20260828_report.json`
- `ann_external_231157_neutral_archive_v0_1.npz`
- `ann_external_231316_neutral_archive_v0_1.npz`
- `ann_external_231543_neutral_archive_v0_1.npz`

The user retains control of all original videos and derived archives.  No
source or archive was deleted, moved, renamed, or otherwise managed after the
run.

