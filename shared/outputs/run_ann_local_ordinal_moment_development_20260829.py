"""Single-shot real development for the frozen local ordinal-moment v2 branch."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

from ann_local_ordinal_moment_v2_0 import (
    OrdinalMomentDevelopmentDecisionA,
    OrdinalMomentKeyA,
    evaluate_frozen_segments,
)


ROOT = Path(__file__).resolve().parent
TASK_ROOT = ROOT.parent
PYAV_RUNTIME = TASK_ROOT / "work" / "pyav_ordinal_15_1_0"
ARCHIVE_ROOT = TASK_ROOT / "work" / "ann_local_ordinal_moment_development_20260829"
MANIFEST = ROOT / "A_ANN_LOCAL_ORDINAL_MOMENT_DEVELOPMENT_ROLE_MANIFEST_V3_20260829.md"
CHARTER = ROOT / "A_ANN_LOCAL_ORDINAL_MOMENT_BRANCH_CHARTER_V2.md"
MODULE = ROOT / "ann_local_ordinal_moment_v2_0.py"
TESTS = ROOT / "test_ann_local_ordinal_moment_v2_0.py"
RUNNER_TESTS = ROOT / "test_run_ann_local_ordinal_moment_development_20260829.py"
ATTEMPT = ROOT / "ann_local_ordinal_moment_development_20260829_attempt.json"
REPORT = ROOT / "ann_local_ordinal_moment_development_20260829_report.json"

EXPECTED_MANIFEST_SHA256 = "151C20F0BE6D8BFE51EE68E417F446EF7CB2C6A2A1EBB4A7039853E3DB6C55FF"
EXPECTED_CHARTER_SHA256 = "58C94D46732C5A2751A6B6797EAC17C446EE18AF3DC7BE9041D3F911F3B6F095"
EXPECTED_MODULE_SHA256 = "F08C1CB633941F5C3640638464CD4C7BD352E1D42382E4845C6A3746E38A9857"
EXPECTED_TEST_SHA256 = "0EFB05A7CB50E7498477A4993C7AFA1353FFB1319689E9DFFCFD5F46A6A5E580"
EXPECTED_RUNNER_TEST_SHA256 = "B4CC15F174B9FC3C883C5426D00EC46D22B02282B6707ADD6D4255D53766DF79"

TARGET_SAMPLE_RATE = 16_000
WINDOW_MS = 100
WINDOW_COUNT = 64
SAMPLES_PER_WINDOW = TARGET_SAMPLE_RATE * WINDOW_MS // 1000
REQUIRED_SAMPLES = WINDOW_COUNT * SAMPLES_PER_WINDOW

SOURCES = (
    {
        "role": "F1",
        "group": "formation",
        "path": Path(r"C:\Users\termi\Videos\螢幕錄製內容\螢幕錄製 2026-08-29 085119.mp4"),
        "bytes": 3_219_554,
        "sha256": "C6C32232576DCB704A26BF9397C75452F328606EE8CD407C3D65AABBFB49FD56",
    },
    {
        "role": "F2",
        "group": "formation",
        "path": Path(r"C:\Users\termi\Videos\螢幕錄製內容\螢幕錄製 2026-08-29 085324.mp4"),
        "bytes": 2_862_206,
        "sha256": "496FFB1096DE1B334A7331AC0359452FF14D495191ACC8501A3A2FE935FA0A4B",
    },
    {
        "role": "F3",
        "group": "formation",
        "path": Path(r"C:\Users\termi\Videos\螢幕錄製內容\螢幕錄製 2026-08-29 085446.mp4"),
        "bytes": 2_714_332,
        "sha256": "71E8D51B9DFB4E43D6DA6DC596C3682E8D254162A7CB1B7D69B57246EFB1B347",
    },
    {
        "role": "H1",
        "group": "heldout",
        "path": Path(r"C:\Users\termi\Videos\螢幕錄製內容\螢幕錄製 2026-08-29 085609.mp4"),
        "bytes": 2_924_466,
        "sha256": "AC237E217F7167FF1C48E051CEE66253FD1D2A55E2C53804159BB5D2AC487121",
    },
    {
        "role": "H2",
        "group": "heldout",
        "path": Path(r"C:\Users\termi\Videos\螢幕錄製內容\螢幕錄製 2026-08-29 085942.mp4"),
        "bytes": 2_404_856,
        "sha256": "B3ECBE95229F965A679AD73924F267B5419DA1348494ECDB14CBD1674532299B",
    },
    {
        "role": "H3",
        "group": "heldout",
        "path": Path(r"C:\Users\termi\Videos\螢幕錄製內容\螢幕錄製 2026-08-29 090039.mp4"),
        "bytes": 2_811_138,
        "sha256": "EBAA321AB60114661461B15D6DD273D0E485E4D2FDAA5A5085E0C8129CB226EF",
    },
)


def sha256_upper(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def pcm_from_resampled_chunks(
    chunks: Iterable[np.ndarray], required_samples: int = REQUIRED_SAMPLES
) -> np.ndarray:
    """Join neutral float32 chunks and return exactly the frozen prefix."""
    if required_samples <= 0:
        raise ValueError("required sample capacity must be positive")
    normalized = []
    channel_count = None
    total = 0
    for chunk in chunks:
        values = np.asarray(chunk)
        if values.dtype != np.float32 or values.ndim != 2 or values.shape[1] <= 0:
            raise ValueError("decoded chunks must be float32 [sample, channel]")
        if not np.all(np.isfinite(values)):
            raise ValueError("decoded PCM must be finite")
        if channel_count is None:
            channel_count = values.shape[1]
        elif values.shape[1] != channel_count:
            raise ValueError("audio channel layout changed during one source")
        if values.shape[0]:
            normalized.append(np.ascontiguousarray(values))
            total += values.shape[0]
        if total >= required_samples:
            break
    if not normalized or total < required_samples:
        raise ValueError("source has fewer than 64 complete 100 ms audio windows")
    return np.ascontiguousarray(np.concatenate(normalized, axis=0)[:required_samples])


def _frame_values(converted) -> np.ndarray:
    values = converted.to_ndarray().astype(np.float32, copy=False).T.copy()
    if values.ndim == 1:
        values = values[:, None]
    return values


def decode_audio_segment_once(av_module, source: dict, archive_path: Path):
    chunks = []
    decoded_sample_count = 0
    source_layout = None
    with av_module.open(str(source["path"]), mode="r") as container:
        if not container.streams.audio:
            raise ValueError(f"{source['role']} has no audio stream")
        stream = container.streams.audio[0]
        source_layout = stream.codec_context.layout.name
        resampler = av_module.AudioResampler(
            format="fltp", layout=source_layout, rate=TARGET_SAMPLE_RATE
        )
        enough = False
        for frame in container.decode(stream):
            for converted in resampler.resample(frame):
                values = _frame_values(converted)
                chunks.append(values)
                decoded_sample_count += values.shape[0]
                if decoded_sample_count >= REQUIRED_SAMPLES:
                    enough = True
                    break
            if enough:
                break
        if not enough:
            for converted in resampler.resample(None):
                values = _frame_values(converted)
                chunks.append(values)
                decoded_sample_count += values.shape[0]
                if decoded_sample_count >= REQUIRED_SAMPLES:
                    break
    pcm = pcm_from_resampled_chunks(chunks)
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        archive_path,
        pcm_f32=pcm,
        sample_rate_i64=np.asarray(TARGET_SAMPLE_RATE, dtype=np.int64),
        source_sha256_u8=np.frombuffer(source["sha256"].encode("ascii"), dtype=np.uint8),
        role_u8=np.frombuffer(source["role"].encode("ascii"), dtype=np.uint8),
    )
    return pcm, {
        "role": source["role"],
        "group": source["group"],
        "source_path": str(source["path"]),
        "source_sha256": source["sha256"],
        "archive_path": str(archive_path),
        "decoder_invocation_count": 1,
        "video_stream_decoded": False,
        "source_audio_layout": source_layout,
        "output_sample_rate": TARGET_SAMPLE_RATE,
        "output_channel_count": int(pcm.shape[1]),
        "decoded_samples_before_frozen_cut": decoded_sample_count,
        "frozen_sample_count": int(pcm.shape[0]),
    }


def _key_rows(keys: Iterable[OrdinalMomentKeyA]):
    return [
        {"carrier_even": key.carrier_even, "arrow_odd": key.arrow_odd}
        for key in sorted(keys)
    ]


def decision_payload(decision: OrdinalMomentDevelopmentDecisionA) -> dict:
    return {
        "decision": decision.decision,
        "reason": decision.reason,
        "formation_dictionary_count": len(decision.formation_dictionary),
        "formation_dictionary": _key_rows(decision.formation_dictionary),
        "forward_supported_count": len(decision.forward_supported),
        "forward_supported": _key_rows(decision.forward_supported),
        "reverse_supported_count": len(decision.reverse_supported),
        "reverse_supported": _key_rows(decision.reverse_supported),
        "per_heldout_forward": list(decision.per_heldout_forward),
        "per_heldout_reverse": list(decision.per_heldout_reverse),
        "formation_three_of_three_count": len(decision.formation_three_of_three),
        "formation_three_of_three": _key_rows(decision.formation_three_of_three),
        "heldout_three_of_three_count": len(decision.heldout_three_of_three),
        "heldout_three_of_three": _key_rows(decision.heldout_three_of_three),
        "formation_occurrence_capacity": list(decision.formation_occurrence_capacity),
        "heldout_occurrence_capacity": list(decision.heldout_occurrence_capacity),
        "formation_distinct_key_counts": list(decision.formation_distinct_key_counts),
        "heldout_distinct_key_counts": list(decision.heldout_distinct_key_counts),
        "formation_zero_arrow_counts": list(decision.formation_zero_arrow_counts),
        "heldout_zero_arrow_counts": list(decision.heldout_zero_arrow_counts),
        "control_support_counts": [
            {"control": name, "support_count": count}
            for name, count in decision.control_support_counts
        ],
        "maximum_control_support_count": max(
            (count for _, count in decision.control_support_counts), default=0
        ),
        "raw_reversal_identity_valid": decision.raw_reversal_identity_valid,
        "pcm_invariants_valid": decision.pcm_invariants_valid,
        "exact_evidence_disjoint": decision.exact_evidence_disjoint,
    }


def _preflight() -> None:
    if ATTEMPT.exists() or REPORT.exists():
        raise FileExistsError("development already started or completed; refusing rerun")
    if not PYAV_RUNTIME.is_dir():
        raise FileNotFoundError(PYAV_RUNTIME)
    expected_files = (
        (MANIFEST, EXPECTED_MANIFEST_SHA256),
        (CHARTER, EXPECTED_CHARTER_SHA256),
        (MODULE, EXPECTED_MODULE_SHA256),
        (TESTS, EXPECTED_TEST_SHA256),
        (RUNNER_TESTS, EXPECTED_RUNNER_TEST_SHA256),
    )
    for path, expected in expected_files:
        if sha256_upper(path) != expected:
            raise RuntimeError(f"frozen file hash changed: {path.name}")
    observed_hashes = []
    for source in SOURCES:
        path = source["path"]
        archive = ARCHIVE_ROOT / f"{source['role']}_neutral_pcm_v1.npz"
        if archive.exists():
            raise FileExistsError(f"neutral derivative already exists: {archive}")
        if not path.is_file() or path.stat().st_size != source["bytes"]:
            raise RuntimeError(f"source path or size changed: {source['role']}")
        observed = sha256_upper(path)
        if observed != source["sha256"]:
            raise RuntimeError(f"source hash changed: {source['role']}")
        observed_hashes.append(observed)
    if len(set(observed_hashes)) != len(SOURCES):
        raise RuntimeError("development source container hashes are not distinct")


def _write_json_exclusive(path: Path, payload: dict) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def main() -> None:
    _preflight()
    sys.path.insert(0, str(PYAV_RUNTIME))
    import av  # type: ignore

    if av.__version__ != "15.1.0" or not hasattr(av, "open"):
        raise RuntimeError("frozen PyAV 15.1.0 runtime is unavailable")
    runner_hash = sha256_upper(Path(__file__).resolve())
    attempt = {
        "schema": "ANN-local-ordinal-moment-development-attempt-v1",
        "status": "started-before-first-source-audio-open",
        "manifest": MANIFEST.name,
        "manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "charter_sha256": EXPECTED_CHARTER_SHA256,
        "module_sha256": EXPECTED_MODULE_SHA256,
        "tests_sha256": EXPECTED_TEST_SHA256,
        "runner_tests_sha256": EXPECTED_RUNNER_TEST_SHA256,
        "runner_sha256": runner_hash,
        "pyav_version": av.__version__,
        "target_sample_rate": TARGET_SAMPLE_RATE,
        "samples_per_window": SAMPLES_PER_WINDOW,
        "window_count": WINDOW_COUNT,
        "source_roles": [
            {
                "role": source["role"],
                "group": source["group"],
                "source_sha256": source["sha256"],
            }
            for source in SOURCES
        ],
        "external_sources_supplied": False,
    }
    _write_json_exclusive(ATTEMPT, attempt)

    decoded = []
    segments = []
    try:
        for source in SOURCES:
            archive = ARCHIVE_ROOT / f"{source['role']}_neutral_pcm_v1.npz"
            pcm, details = decode_audio_segment_once(av, source, archive)
            segments.append(pcm)
            decoded.append(details)
        channel_counts = {segment.shape[1] for segment in segments}
        if len(channel_counts) != 1:
            raise ValueError("development source channel counts are incompatible")
        decision = evaluate_frozen_segments(
            tuple(segments[:3]), tuple(segments[3:]), SAMPLES_PER_WINDOW
        )
        report = {
            "schema": "ANN-local-ordinal-moment-development-v1",
            "development_only": True,
            "attempt_marker": ATTEMPT.name,
            "attempt_marker_sha256": sha256_upper(ATTEMPT),
            "manifest": MANIFEST.name,
            "manifest_sha256": EXPECTED_MANIFEST_SHA256,
            "runner_sha256": runner_hash,
            "decode": decoded,
            "result": decision_payload(decision),
            "external_sources_supplied": False,
            "external_source_read": False,
            "active_reader_modified": False,
            "rerun_allowed": False,
        }
    except Exception as error:
        report = {
            "schema": "ANN-local-ordinal-moment-development-v1",
            "development_only": True,
            "attempt_marker": ATTEMPT.name,
            "attempt_marker_sha256": sha256_upper(ATTEMPT),
            "manifest": MANIFEST.name,
            "manifest_sha256": EXPECTED_MANIFEST_SHA256,
            "runner_sha256": runner_hash,
            "decode": decoded,
            "result": {
                "decision": "inconclusive-structural-or-io-incompatibility",
                "error_type": type(error).__name__,
                "reason": str(error),
            },
            "external_sources_supplied": False,
            "external_source_read": False,
            "active_reader_modified": False,
            "rerun_allowed": False,
        }
    _write_json_exclusive(REPORT, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

