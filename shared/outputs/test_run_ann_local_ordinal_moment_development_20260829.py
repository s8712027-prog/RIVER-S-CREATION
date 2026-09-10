from __future__ import annotations

import unittest

import numpy as np

import run_ann_local_ordinal_moment_development_20260829 as runner
from ann_local_ordinal_moment_v2_0 import (
    OrdinalMomentDevelopmentDecisionA,
    OrdinalMomentKeyA,
)


class LocalOrdinalMomentDevelopmentRunnerTests(unittest.TestCase):
    def test_frozen_geometry_and_roles(self):
        self.assertEqual(runner.TARGET_SAMPLE_RATE, 16_000)
        self.assertEqual(runner.SAMPLES_PER_WINDOW, 1_600)
        self.assertEqual(runner.WINDOW_COUNT, 64)
        self.assertEqual(runner.REQUIRED_SAMPLES, 102_400)
        self.assertEqual(
            tuple(item["role"] for item in runner.SOURCES),
            ("F1", "F2", "F3", "H1", "H2", "H3"),
        )
        self.assertEqual(
            tuple(item["group"] for item in runner.SOURCES),
            ("formation", "formation", "formation", "heldout", "heldout", "heldout"),
        )
        names = tuple(item["path"].name for item in runner.SOURCES)
        self.assertNotIn("螢幕錄製 2026-08-29 085250.mp4", names)
        self.assertTrue(all(" 08" in name or " 090039" in name for name in names))
        self.assertEqual(len({item["sha256"] for item in runner.SOURCES}), 6)

    def test_frozen_local_file_hashes_match(self):
        self.assertEqual(runner.sha256_upper(runner.MANIFEST), runner.EXPECTED_MANIFEST_SHA256)
        self.assertEqual(runner.sha256_upper(runner.CHARTER), runner.EXPECTED_CHARTER_SHA256)
        self.assertEqual(runner.sha256_upper(runner.MODULE), runner.EXPECTED_MODULE_SHA256)
        self.assertEqual(runner.sha256_upper(runner.TESTS), runner.EXPECTED_TEST_SHA256)

    def test_pcm_chunk_join_is_exact_and_bounded(self):
        first = np.arange(18, dtype=np.float32).reshape(9, 2)
        second = np.arange(18, 38, dtype=np.float32).reshape(10, 2)
        result = runner.pcm_from_resampled_chunks((first, second), required_samples=12)
        expected = np.concatenate((first, second), axis=0)[:12]
        self.assertEqual(result.dtype, np.float32)
        self.assertTrue(result.flags.c_contiguous)
        self.assertTrue(np.array_equal(result, expected))

    def test_pcm_chunk_join_rejects_structural_failures(self):
        good = np.zeros((4, 2), dtype=np.float32)
        with self.assertRaises(ValueError):
            runner.pcm_from_resampled_chunks((good,), required_samples=5)
        with self.assertRaises(ValueError):
            runner.pcm_from_resampled_chunks((good.astype(np.float64),), required_samples=1)
        with self.assertRaises(ValueError):
            runner.pcm_from_resampled_chunks(
                (good, np.zeros((4, 1), dtype=np.float32)), required_samples=8
            )
        bad = good.copy()
        bad[0, 0] = np.nan
        with self.assertRaises(ValueError):
            runner.pcm_from_resampled_chunks((bad,), required_samples=1)

    def test_decision_payload_preserves_all_frozen_reports(self):
        one = OrdinalMomentKeyA(4, 2)
        two = OrdinalMomentKeyA(6, -2)
        decision = OrdinalMomentDevelopmentDecisionA(
            "retain-development-candidate",
            frozenset((one, two)),
            frozenset((one, two)),
            frozenset(),
            (2, 2, 2),
            (0, 0, 0),
            frozenset((one,)),
            frozenset((two,)),
            (128, 128, 128),
            (128, 128, 128),
            (20, 21, 22),
            (23, 24, 25),
            (1, 2, 3),
            (4, 5, 6),
            (("adjacency:a2-b0", 1), ("linkage:shift-01", 0)),
            True,
            True,
            True,
            "fixture",
        )
        payload = runner.decision_payload(decision)
        self.assertEqual(payload["forward_supported_count"], 2)
        self.assertEqual(payload["reverse_supported_count"], 0)
        self.assertEqual(payload["maximum_control_support_count"], 1)
        self.assertEqual(payload["formation_occurrence_capacity"], [128, 128, 128])
        self.assertEqual(payload["heldout_zero_arrow_counts"], [4, 5, 6])
        self.assertTrue(payload["raw_reversal_identity_valid"])


if __name__ == "__main__":
    unittest.main()

