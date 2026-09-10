# ANN/A PyAV permanent runtime repair — 2026-08-29

## Outcome

The repeated PyAV initialization failure is repaired at the shared neutral AV
decoder, not only in the latest ingest runner.

The actual cause was filesystem ACL damage in the historical runtime folders.
Python could see their `av` directory names but could not read their contents,
so `import av` returned an empty namespace without `av.open`.  Every new
process therefore failed again.

## Permanent repair

1. PyAV 15.1.0 was installed into the environment-managed Codex primary Python
   site-packages, which is available across turns:

   `C:\Users\termi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages`

2. The shared decoder was changed to search in this order:

   - `ANN_PYAV_RUNTIME`, when explicitly configured;
   - the Codex primary-runtime site-packages;
   - the shared-workspace `pyav_runtime_fixed` fallback;
   - decoder-local `_pyav_runtime_fixed`;
   - the historical runtime directories as fallbacks only.

3. The single-material runner no longer preloads a private PyAV workaround.
   It now exercises the same repaired decoder path as existing runners.

## Verification

A completely new Python process imported the shared decoder and instantiated
`SynchronizedAVDecoderA` successfully:

`standalone-decoder-ok 15.1.0 True`

The integration regression now instantiates the real decoder and asserts that
`av.open` exists, so a future empty-namespace regression cannot pass silently.
The complete ANN/A local unit suite passed 263/263 after the decoder repair
and now passes 267/267 after the M2 persistence integration.

No user video was decoded during this repair verification.  The three 09:51–
09:57 videos had already completed their successful one-shot decodes before
this permanent runtime consolidation.

## Scope

This resolves the recurring local PyAV availability problem for callers of
`synchronized_av_decoder_v0_1.py`.  It does not install PyAV globally and does
not modify system Python.  Historical unreadable runtime directories remain
untouched and are no longer the preferred path.

An attempted Python user-site installation was rejected by the host Windows
ACL before package installation.  The shared-workspace runtime is therefore
the persistent usable location; it does not rely on per-turn access to either
historical model project.

The repair was then exercised on a later attachment turn, not merely in the
installation turn.  After a pre-decode failure exposed the remaining
decoder-project permission dependency, the decoder selected the shared
runtime in a fresh process and successfully decoded the new 101128, 101506,
and 103439 sources sequentially.  This is the first cross-turn operational
confirmation of the final runtime location.

