# ANN/A local ordinal-moment new-material role manifest template v2

## Purpose

This template freezes source roles before any decode or feature read for the
local ordinal-moment v2 branch.  Completing the table does not activate the
candidate and does not authorize use of any earlier material.

## Material boundary

Supply nine wholly new, independently recorded sources.  Each should contain
at least 6.4 seconds of usable audio; recording at least 8 seconds with the
same capture setup is recommended so container start-up does not consume the
fixed observation budget.

The following are permanently excluded from this branch:

- the old eleven development sources;
- the failed external-validation group, including
  `螢幕錄製 2026-08-28 231157.mp4`,
  `螢幕錄製 2026-08-28 231316.mp4`, and
  `螢幕錄製 2026-08-28 231543.mp4`;
- `螢幕錄製 2026-08-28 233248.mp4`;
- `螢幕錄製 2026-08-28 233446.mp4`;
- any copy, transcode, excerpt, or derivative of an excluded source.

Sort the nine new sources by actual recording acquisition order before opening
or decoding any of them.  Freeze roles exactly as follows; do not choose roles
from observed audio content or model output.

| Acquisition order | Frozen role | Absolute path | Recording start/time evidence | File SHA-256 | State |
|---:|---|---|---|---|---|
| 1 | F1 formation | _unfilled_ | _unfilled_ | _uncomputed_ | unopened |
| 2 | F2 formation | _unfilled_ | _unfilled_ | _uncomputed_ | unopened |
| 3 | F3 formation | _unfilled_ | _unfilled_ | _uncomputed_ | unopened |
| 4 | H1 held-out development | _unfilled_ | _unfilled_ | _uncomputed_ | unopened |
| 5 | H2 held-out development | _unfilled_ | _unfilled_ | _uncomputed_ | unopened |
| 6 | H3 held-out development | _unfilled_ | _unfilled_ | _uncomputed_ | unopened |
| 7 | X1 sealed external | _unfilled_ | _unfilled_ | _uncomputed_ | sealed/unopened |
| 8 | X2 sealed external | _unfilled_ | _unfilled_ | _uncomputed_ | sealed/unopened |
| 9 | X3 sealed external | _unfilled_ | _unfilled_ | _uncomputed_ | sealed/unopened |

If acquisition order is genuinely ambiguous, the user must declare the order
before any metadata beyond filename/path and raw file hash is inspected.

## Pre-decode freeze record

Fill these fields only after all nine roles above are fixed:

- charter path: `outputs/A_ANN_LOCAL_ORDINAL_MOMENT_BRANCH_CHARTER_V2.md`
- charter SHA-256: _unfilled_
- implementation path: `outputs/ann_local_ordinal_moment_v2_0.py`
- implementation SHA-256: _unfilled_
- test path: `outputs/test_ann_local_ordinal_moment_v2_0.py`
- test SHA-256: _unfilled_
- role-manifest SHA-256: _recorded in the separate attempt marker only after
  the instantiated manifest is final; never written back into the hashed file_
- fixed window geometry: first 64 contiguous complete 100 ms windows
- frozen public evaluator: `evaluate_frozen_segments`
- formation count: 3
- held-out development count: 3
- sealed external count: 3
- freeze timestamp with timezone: _unfilled_

Computing the raw file SHA-256 is allowed after role assignment because it does
not decode audio.  F1–F3 and H1–H3 may each receive exactly one neutral decode
only after the complete attempt marker is durably written.  X1–X3 remain
sealed: hash their containers, but do not decode, preview, sample, or
feature-read them unless development first passes.

## Compatibility and single-shot rules

- F1–F3 and H1–H3 must expose compatible sample rate and channel layout after
  their one neutral decode.
- The evaluator receives finite neutral `float32` PCM, preserving channels.
- Only the first 64 complete contiguous 100 ms windows are eligible.
- Structural inability to construct equal-capacity inputs is Inconclusive;
  unfavorable scores or failed invariants are Fail.
- Do not replace an inconvenient source, change roles, tune the representation,
  or rerun development after any feature or score is observed.
- If development fails, X1–X3 remain unopened and this branch stops.
- If development passes, external validation is a separate one-shot operation
  with a separately frozen marker.  A development pass does not itself
  authorize activation of the candidate.

## Current state

This is an unfilled template.  No listed source exists yet, no role has been
assigned, and no real-data run is authorized.

