# ANN/A local ordinal-moment development result — 2026-08-29

## Outcome

The frozen local ordinal-moment v2 development candidate is **rejected**.
This was a valid empirical Fail, not an I/O or structural Inconclusive result.
The active provisional local-capability reader remains unchanged.

Six newly supplied recordings were reset by explicit user authorization into
F1–F3 formation and H1–H3 held-out roles.  Each source audio stream was opened
and decoded exactly once.  No video stream, old source, previous development
source, failed external source, unmentioned 085250 file, or external X source
was decoded or feature-read.

## Frozen execution

- role manifest SHA-256:
  `151C20F0BE6D8BFE51EE68E417F446EF7CB2C6A2A1EBB4A7039853E3DB6C55FF`;
- candidate implementation SHA-256:
  `F08C1CB633941F5C3640638464CD4C7BD352E1D42382E4845C6A3746E38A9857`;
- runner SHA-256:
  `B52585DB06ABB54ABBE2A7D705602D92B4C2BD4C755771D9D48037ED5AE5FA08`;
- attempt marker SHA-256:
  `D686912C9CE3C2AF948A57570AFC70DDCAD67B6C2D3C33FCC3874CEDEDDCB051`;
- result JSON SHA-256:
  `017B5DFF5B5B72C387B42A347CF8EAF1426B4C2B44BF832EC7019D8C477AE295`.

The first runner invocation stopped before the attempt marker and before any
source open because the earlier PyAV directory exposed only an unusable
namespace.  A fresh isolated PyAV 15.1.0 runtime was installed, the runtime
path alone was corrected, 24/24 candidate-plus-runner tests passed, and the
final hashed runner performed the only data execution.

Every source produced one finite stereo neutral derivative with shape
`[102400, 2]`, dtype `float32`, and sample rate 16,000 Hz.  This is exactly 64
contiguous 100 ms windows per source.  All six original container hashes were
distinct.

## Frozen decision evidence

| Quantity | Result |
|---|---:|
| Formation dictionary | 18 oriented keys |
| Forward keys recurrent in at least 2/3 held-out sources | 0 |
| Aggregate raw-reverse recurrent keys | 0 |
| Individual controls | 59 |
| Maximum individual control support | 2 |
| Per-source forward H1 / H2 / H3 | 0 / 2 / 1 |
| Per-source reverse H1 / H2 / H3 | 1 / 3 / 0 |
| Formation occurrence capacity | 128 / 128 / 128 |
| Held-out occurrence capacity | 128 / 128 / 128 |
| Formation distinct keys | 124 / 122 / 64 |
| Held-out distinct keys | 63 / 121 / 120 |
| Formation `F=0` occurrences | 2 / 4 / 2 |
| Held-out `F=0` occurrences | 4 / 4 / 3 |
| Raw-reversal identity | pass |
| PCM polarity/channel invariants | pass |
| Exact evidence disjointness | pass |

The candidate fails several frozen requirements independently:

- forward support `S=0`, below the required minimum `S>=2`;
- forward ties aggregate reverse at zero rather than strictly exceeding it;
- several adjacency controls score above forward, with maximum 2;
- H1 and H2 do not individually beat their raw reversals.

The failure is therefore not caused by insufficient duration, incompatible
channels, a malformed control, reversal algebra, duplicated evidence, or a
decoder failure.  Eighteen oriented keys recur during formation, but no one of
them recurs in at least two held-out sources.  The bounded interpretation is
that this representation remains insufficiently source-transferable.

## Binding consequence

- Do not rerun this attempt or replace/reorder any of its six sources.
- Do not tune microbins, windows, ranks, moments, incidence thresholds, or
  controls on these neutral derivatives.
- Do not provide or decode X1–X3 for this rejected branch; external validation
  is not reached.
- Keep ordinal-moment v2 inactive and keep the provisional reader unchanged.
- The six neutral PCM derivatives may be retained only as immutable audit
  evidence; they are not authorized development material for another variant.

## Result files

- `ann_local_ordinal_moment_development_20260829_attempt.json`
- `ann_local_ordinal_moment_development_20260829_report.json`
- `A_ANN_LOCAL_ORDINAL_MOMENT_DEVELOPMENT_ROLE_MANIFEST_V3_20260829.md`
- `run_ann_local_ordinal_moment_development_20260829.py`
- `test_run_ann_local_ordinal_moment_development_20260829.py`

