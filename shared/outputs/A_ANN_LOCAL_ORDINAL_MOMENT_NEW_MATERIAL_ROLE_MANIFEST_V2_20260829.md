# ANN/A local ordinal-moment new-material role manifest v2 — 2026-08-29

## State

Four of nine required new source paths have been supplied and irrevocably
role-ordered from their recording timestamps.  They are registered from the
user's message only.  None of the four files has been opened, hashed, probed,
previewed, decoded, sampled, or feature-read.

The development run remains unauthorized.  H2, H3, X1, X2, and X3 are still
missing.  All nine roles and raw container hashes must be present in a final
manifest and attempt marker before F1 is loaded.

## Frozen acquisition-order roles

| Acquisition order | Frozen role | User-supplied absolute path | Time evidence from filename | Container hash | State |
|---:|---|---|---|---|---|
| 1 | F1 formation | `C:\Users\termi\Videos\螢幕錄製內容\螢幕錄製 2026-08-29 030156.mp4` | 2026-08-29 03:01:56 | not read | role-frozen, unopened |
| 2 | F2 formation | `C:\Users\termi\Videos\螢幕錄製內容\螢幕錄製 2026-08-29 030437.mp4` | 2026-08-29 03:04:37 | not read | role-frozen, unopened |
| 3 | F3 formation | `C:\Users\termi\Videos\螢幕錄製內容\螢幕錄製 2026-08-29 030634.mp4` | 2026-08-29 03:06:34 | not read | role-frozen, unopened |
| 4 | H1 held-out development | `C:\Users\termi\Videos\螢幕錄製內容\螢幕錄製 2026-08-29 032547.mp4` | 2026-08-29 03:25:47 | not read | role-frozen, unopened |
| 5 | H2 held-out development | _missing_ | _missing_ | not read | not supplied |
| 6 | H3 held-out development | _missing_ | _missing_ | not read | not supplied |
| 7 | X1 sealed external | _missing_ | _missing_ | not read | sealed role not supplied |
| 8 | X2 sealed external | _missing_ | _missing_ | not read | sealed role not supplied |
| 9 | X3 sealed external | _missing_ | _missing_ | not read | sealed role not supplied |

The four existing role assignments cannot be changed after later files are
provided.  Future files occupy acquisition orders 5–9.  If any registered file
is a copy, transcode, excerpt, continuation split from another source, too
short, or structurally incompatible, the one-shot development construction is
Inconclusive; do not replace it after inspection.

## Frozen branch snapshot

- charter: `A_ANN_LOCAL_ORDINAL_MOMENT_BRANCH_CHARTER_V2.md`
- charter SHA-256:
  `58C94D46732C5A2751A6B6797EAC17C446EE18AF3DC7BE9041D3F911F3B6F095`
- implementation: `ann_local_ordinal_moment_v2_0.py`
- implementation SHA-256:
  `F08C1CB633941F5C3640638464CD4C7BD352E1D42382E4845C6A3746E38A9857`
- tests: `test_ann_local_ordinal_moment_v2_0.py`
- tests SHA-256:
  `0EFB05A7CB50E7498477A4993C7AFA1353FFB1319689E9DFFCFD5F46A6A5E580`
- active provisional reader remains separate and unchanged:
  `74AAA1AF2AACAD0FF8B13DF5DD9D472CBE91F95D07C87F9F773352FF0DD81ACA`
- observation: first 64 complete contiguous 100 ms windows;
- public synthetic evaluator: `evaluate_frozen_segments`;
- control manifest: raw reverse + 28 adjacency + 31 linkage controls;
- candidate state: isolated development candidate, inactive.

## Completion procedure

When the remaining five paths are supplied:

1. Register them as H2, H3, X1, X2, X3 strictly by acquisition order, without
   opening any file.
2. Finalize this manifest and compute its SHA-256 externally; record that hash
   in a separate immutable attempt marker rather than inside this file.
3. Compute raw container SHA-256 values only after all roles are fixed.  All
   nine hashes must be distinct.
4. Write the complete attempt marker containing source roles and hashes, the
   frozen branch hashes, geometry, controls, and one-shot state.
5. Decode F1–F3 and H1–H3 once to finite channel-preserving neutral `float32`
   PCM.  Do not decode or inspect X1–X3.
6. If compatible equal-capacity development inputs cannot be constructed,
   record Inconclusive and stop without replacement or tuning.
7. Otherwise run the frozen development evaluator once.  On Fail, leave
   X1–X3 sealed and stop.  A Pass permits a separately marked single external
   validation; it does not activate the candidate automatically.

## Exclusions

The old eleven, the 2026-08-28 231157/231316/231543 failed-external group, the
2026-08-28 233248/233446 development pair, and all of their copies or
derivatives remain forbidden.

