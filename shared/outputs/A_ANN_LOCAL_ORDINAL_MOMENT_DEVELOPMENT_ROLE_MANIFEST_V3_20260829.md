# ANN/A local ordinal-moment development role manifest v3 — 2026-08-29

## Authority and reset

The user explicitly authorized running development now and supplying external
validation later.  The four earlier 03:01–03:25 paths were unavailable before
any hash, decode, feature, or score was obtained from them.  They are therefore
retired from this unstarted attempt.  This manifest resets the six available,
user-supplied 08:51–09:00 recordings by acquisition order as the complete
development set.

The unmentioned `螢幕錄製 2026-08-29 085250.mp4` is not a supplied source and is
excluded.  No content, hash, stream, or feature is to be read from it.

## Frozen development roles

| Order | Role | Absolute source path | Bytes | SHA-256 |
|---:|---|---|---:|---|
| 1 | F1 formation | `C:\Users\termi\Videos\螢幕錄製內容\螢幕錄製 2026-08-29 085119.mp4` | 3,219,554 | `C6C32232576DCB704A26BF9397C75452F328606EE8CD407C3D65AABBFB49FD56` |
| 2 | F2 formation | `C:\Users\termi\Videos\螢幕錄製內容\螢幕錄製 2026-08-29 085324.mp4` | 2,862,206 | `496FFB1096DE1B334A7331AC0359452FF14D495191ACC8501A3A2FE935FA0A4B` |
| 3 | F3 formation | `C:\Users\termi\Videos\螢幕錄製內容\螢幕錄製 2026-08-29 085446.mp4` | 2,714,332 | `71E8D51B9DFB4E43D6DA6DC596C3682E8D254162A7CB1B7D69B57246EFB1B347` |
| 4 | H1 held-out development | `C:\Users\termi\Videos\螢幕錄製內容\螢幕錄製 2026-08-29 085609.mp4` | 2,924,466 | `AC237E217F7167FF1C48E051CEE66253FD1D2A55E2C53804159BB5D2AC487121` |
| 5 | H2 held-out development | `C:\Users\termi\Videos\螢幕錄製內容\螢幕錄製 2026-08-29 085942.mp4` | 2,404,856 | `B3ECBE95229F965A679AD73924F267B5419DA1348494ECDB14CBD1674532299B` |
| 6 | H3 held-out development | `C:\Users\termi\Videos\螢幕錄製內容\螢幕錄製 2026-08-29 090039.mp4` | 2,811,138 | `EBAA321AB60114661461B15D6DD273D0E485E4D2FDAA5A5085E0C8129CB226EF` |

All six container hashes are distinct.  Roles may not change after this file.

## External boundary

X1–X3 are not yet supplied.  Development may run once under the user's explicit
override, but no external claim can be made.  If development rejects or is
Inconclusive, later X files remain unused.  If development retains the
candidate, three wholly new X recordings must be role-frozen and sealed before
any external decode.

## Frozen representation snapshot

- charter: `A_ANN_LOCAL_ORDINAL_MOMENT_BRANCH_CHARTER_V2.md`
- charter SHA-256:
  `58C94D46732C5A2751A6B6797EAC17C446EE18AF3DC7BE9041D3F911F3B6F095`
- implementation: `ann_local_ordinal_moment_v2_0.py`
- implementation SHA-256:
  `F08C1CB633941F5C3640638464CD4C7BD352E1D42382E4845C6A3746E38A9857`
- tests: `test_ann_local_ordinal_moment_v2_0.py`
- tests SHA-256:
  `0EFB05A7CB50E7498477A4993C7AFA1353FFB1319689E9DFFCFD5F46A6A5E580`
- active reader remains separate and unchanged:
  `74AAA1AF2AACAD0FF8B13DF5DD9D472CBE91F95D07C87F9F773352FF0DD81ACA`

## Frozen neutral audio decode

- exactly one audio-stream decode invocation per development source;
- no video-stream decode;
- PyAV 15.1.0;
- first audio stream only;
- resample once to planar `float32` at 16,000 Hz;
- preserve the source channel layout; do not mix channels;
- concatenate decoded audio frames in stream order;
- take exactly the first 102,400 decoded samples per channel;
- interpret them as 64 contiguous 100 ms windows of 1,600 samples;
- reject structurally if any source lacks capacity, finite PCM, or a compatible
  channel count;
- save one neutral PCM derivative per source so the original is never decoded
  again.

## Frozen decision

Use only `evaluate_frozen_segments` from the hashed implementation.  It must
internally derive raw reversal, all 28 adjacency controls, all 31 linkage
controls, capacities, evidence, and PCM invariants.  Pass/Fail/Inconclusive
semantics remain exactly those in the v2 charter.  No tuning, replacement,
rerun, or alternate split is allowed after the first source audio stream opens.

