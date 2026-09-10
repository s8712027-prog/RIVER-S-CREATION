from __future__ import annotations

import itertools
import statistics
import unittest
from collections import Counter

import numpy as np
import ann_local_ordinal_moment_v2_0 as ordinal_module

from ann_local_ordinal_moment_v2_0 import (
    ADJACENCY_CONTROL_ORDERS,
    OrdinalMomentKeyA,
    adjacency_control_key,
    doubled_microbin_medians,
    evaluate_frozen_segments,
    linkage_control_keys,
    ordinal_scores,
    parity_moment_key,
    reverse_pcm_frames,
    roughness_magnitudes,
    segment_occurrences,
    strict_rank_key_census,
)


class LocalOrdinalMomentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rng = np.random.default_rng(20260829)
        cls.samples_per_window = 80
        cls.window_count = 64
        cls.segment = rng.integers(
            -2000,
            2001,
            size=(cls.samples_per_window * cls.window_count, 2),
            dtype=np.int32,
        )

    def test_strict_rank_census_is_frozen_intermediate_compression(self):
        census = strict_rank_key_census()
        independently_observed = Counter(
            parity_moment_key(ranks) for ranks in itertools.permutations(range(7))
        )
        self.assertEqual(census, independently_observed)
        self.assertEqual(sum(census.values()), 5040)
        self.assertEqual(len(census), 1735)
        self.assertEqual(sum(key.oriented for key in census), 1692)
        self.assertEqual(statistics.median(census.values()), 3)
        self.assertEqual(max(census.values()), 13)

    def test_all_weak_orders_are_tie_safe_and_reverse_exactly(self):
        weak_order_count = 0
        for level_count in range(1, 8):
            required = set(range(level_count))
            for values in itertools.product(range(level_count), repeat=7):
                if set(values) != required:
                    continue
                weak_order_count += 1
                scores = ordinal_scores(values)
                reversed_scores = ordinal_scores(tuple(reversed(values)))
                self.assertEqual(sum(scores), 0)
                self.assertEqual(reversed_scores, tuple(reversed(scores)))
                key = parity_moment_key(values)
                self.assertEqual(
                    parity_moment_key(tuple(reversed(values))), key.reversed()
                )
        self.assertEqual(weak_order_count, 47293)

    def test_raw_frame_reversal_recomputes_exact_key_mapping(self):
        forward = segment_occurrences(
            self.segment, self.samples_per_window, self.window_count
        )
        reversed_items = segment_occurrences(
            reverse_pcm_frames(self.segment), self.samples_per_window, self.window_count
        )
        by_coordinate = {
            (item.window_index, item.channel_index): item for item in reversed_items
        }
        for item in forward:
            mirror = by_coordinate[(self.window_count - 1 - item.window_index, item.channel_index)]
            self.assertEqual(mirror.key, item.key.reversed())

    def test_double_reversal_restores_pcm_and_keys(self):
        twice = reverse_pcm_frames(reverse_pcm_frames(self.segment))
        self.assertTrue(np.array_equal(twice, self.segment))
        first = segment_occurrences(
            self.segment, self.samples_per_window, self.window_count
        )
        second = segment_occurrences(
            twice, self.samples_per_window, self.window_count
        )
        self.assertEqual(first, second)

    def test_nonzero_affine_amplitude_transform_preserves_keys(self):
        baseline = [item.key for item in segment_occurrences(
            self.segment, self.samples_per_window, self.window_count
        )]
        transformed = (-3 * self.segment.astype(np.int64) + 17).astype(np.int32)
        observed = [item.key for item in segment_occurrences(
            transformed, self.samples_per_window, self.window_count
        )]
        self.assertEqual(baseline, observed)
        independent = self.segment.copy()
        independent[:, 0] = -3 * independent[:, 0] + 17
        independent[:, 1] = 2 * independent[:, 1] - 5
        independent_keys = [item.key for item in segment_occurrences(
            independent, self.samples_per_window, self.window_count
        )]
        self.assertEqual(baseline, independent_keys)

    def test_float32_median_symmetries_hold_before_key_compression(self):
        window = self.segment[:self.samples_per_window].astype(np.float32)
        forward = doubled_microbin_medians(window)
        reversed_bins = doubled_microbin_medians(window[::-1])
        polarity = doubled_microbin_medians(-window)
        self.assertTrue(np.array_equal(reversed_bins, forward[::-1]))
        self.assertTrue(np.array_equal(polarity, -forward))

    def test_float32_archive_style_pcm_keeps_exact_reversal_mapping(self):
        pcm = self.segment.astype(np.float32) / np.float32(2048.0)
        forward = segment_occurrences(pcm, self.samples_per_window, self.window_count)
        reversed_items = segment_occurrences(
            reverse_pcm_frames(pcm), self.samples_per_window, self.window_count
        )
        by_coordinate = {
            (item.window_index, item.channel_index): item for item in reversed_items
        }
        for item in forward:
            mirror = by_coordinate[(self.window_count - 1 - item.window_index, item.channel_index)]
            self.assertEqual(mirror.key, item.key.reversed())

    def test_channel_permutation_and_duplication_preserve_distinct_keys(self):
        original = segment_occurrences(
            self.segment, self.samples_per_window, self.window_count
        )
        swapped = segment_occurrences(
            self.segment[:, ::-1], self.samples_per_window, self.window_count
        )
        self.assertEqual({item.key for item in original}, {item.key for item in swapped})
        mono = self.segment[:, :1]
        duplicated = np.repeat(mono, 2, axis=1)
        mono_keys = {item.key for item in segment_occurrences(
            mono, self.samples_per_window, self.window_count
        )}
        duplicate_keys = {item.key for item in segment_occurrences(
            duplicated, self.samples_per_window, self.window_count
        )}
        self.assertEqual(mono_keys, duplicate_keys)

    def test_permuting_samples_inside_each_microbin_preserves_keys(self):
        changed = self.segment.copy()
        frames_per_bin = self.samples_per_window // 8
        for window in range(self.window_count):
            base = window * self.samples_per_window
            for microbin in range(8):
                start = base + microbin * frames_per_bin
                stop = start + frames_per_bin
                changed[start:stop] = changed[start:stop][::-1]
        baseline = [item.key for item in segment_occurrences(
            self.segment, self.samples_per_window, self.window_count
        )]
        observed = [item.key for item in segment_occurrences(
            changed, self.samples_per_window, self.window_count
        )]
        self.assertEqual(baseline, observed)

    def test_all_adjacency_controls_preserve_marginals_and_break_neighbors(self):
        self.assertEqual(len(ADJACENCY_CONTROL_ORDERS), 28)
        self.assertEqual(len(set(ADJACENCY_CONTROL_ORDERS)), 28)
        occurrence = segment_occurrences(
            self.segment[:self.samples_per_window], self.samples_per_window, 1
        )[0]
        for order in ADJACENCY_CONTROL_ORDERS:
            self.assertEqual(tuple(sorted(order)), tuple(range(7)))
            self.assertTrue(all(abs(right - left) != 1 for left, right in zip(order, order[1:])))
            permuted = tuple(occurrence.roughness_magnitudes[index] for index in order)
            self.assertCountEqual(permuted, occurrence.roughness_magnitudes)
            self.assertIsInstance(adjacency_control_key(occurrence, order), OrdinalMomentKeyA)

    def test_linkage_control_preserves_carrier_and_arrow_marginals(self):
        occurrences = segment_occurrences(
            self.segment, self.samples_per_window, self.window_count
        )
        self.assertEqual(
            [(item.window_index, item.channel_index) for item in occurrences],
            list(itertools.product(range(self.window_count), range(2))),
        )
        for shift in range(1, 32):
            controlled = linkage_control_keys(occurrences, shift)
            self.assertEqual(len(controlled), len(occurrences))
            self.assertCountEqual(
                (key.carrier_even for key in controlled),
                (item.key.carrier_even for item in occurrences),
            )
            self.assertCountEqual(
                (key.arrow_odd for key in controlled),
                (item.key.arrow_odd for item in occurrences),
            )

    def test_invalid_window_geometry_is_rejected(self):
        with self.assertRaises(ValueError):
            doubled_microbin_medians(np.zeros((79, 2)))
        with self.assertRaises(ValueError):
            segment_occurrences(np.zeros((80, 2)), 80, 64)

    def test_unsupported_pcm_dtypes_are_rejected(self):
        for dtype in (np.float64, np.uint16, np.int64):
            with self.subTest(dtype=dtype):
                with self.assertRaises(ValueError):
                    segment_occurrences(
                        self.segment.astype(dtype),
                        self.samples_per_window,
                        self.window_count,
                    )

    @classmethod
    def affine_distinct_segments(cls):
        transforms = ((1, 0), (-2, 3), (3, -7), (-4, 11), (5, 17), (-6, -13))
        return tuple(
            (scale * cls.segment.astype(np.int64) + offset).astype(np.int32)
            for scale, offset in transforms
        )

    def test_fail_closed_evaluator_internally_builds_all_controls(self):
        sources = self.affine_distinct_segments()
        result = evaluate_frozen_segments(
            sources[:3], sources[3:], self.samples_per_window
        )
        names = tuple(name for name, _ in result.control_support_counts)
        expected_adjacency = tuple(
            f"adjacency:a{multiplier}-b{offset}"
            for multiplier in (2, 3, 4, 5)
            for offset in range(7)
        )
        expected_linkage = tuple(
            f"linkage:shift-{shift:02d}" for shift in range(1, 32)
        )
        self.assertEqual(names, expected_adjacency + expected_linkage)
        self.assertEqual(len(set(names)), 59)
        self.assertTrue(result.raw_reversal_identity_valid)
        self.assertTrue(result.pcm_invariants_valid)
        self.assertTrue(result.exact_evidence_disjoint)
        self.assertEqual(result.formation_three_of_three, result.formation_dictionary)
        self.assertEqual(result.heldout_three_of_three, result.forward_supported)
        self.assertEqual(result.formation_occurrence_capacity, (128, 128, 128))
        self.assertEqual(result.heldout_occurrence_capacity, (128, 128, 128))
        self.assertTrue(all(count > 0 for count in result.formation_distinct_key_counts))
        self.assertTrue(all(count > 0 for count in result.heldout_distinct_key_counts))
        self.assertEqual(len(result.formation_zero_arrow_counts), 3)
        self.assertEqual(len(result.heldout_zero_arrow_counts), 3)
        self.assertEqual(result.decision, "retain-development-candidate")

    def test_frozen_manifest_rebinding_is_rejected(self):
        sources = self.affine_distinct_segments()
        original = ordinal_module.LINKAGE_SHIFT_LIMIT
        try:
            ordinal_module.LINKAGE_SHIFT_LIMIT = 0
            with self.assertRaises(RuntimeError):
                evaluate_frozen_segments(
                    sources[:3], sources[3:], self.samples_per_window
                )
        finally:
            ordinal_module.LINKAGE_SHIFT_LIMIT = original
        self.assertFalse(hasattr(ordinal_module, "_evaluate_frozen_occurrences"))

    def test_duplicate_exact_evidence_forces_rejection(self):
        result = evaluate_frozen_segments(
            (self.segment, self.segment, self.segment),
            (self.segment, self.segment, self.segment),
            self.samples_per_window,
        )
        self.assertFalse(result.exact_evidence_disjoint)
        self.assertEqual(result.decision, "reject-development-candidate")

    def test_one_recurrent_key_is_below_frozen_minimum(self):
        levels = np.cumsum(np.asarray((0, 1, 2, 3, 4, 5, 6, 7), dtype=np.int32))
        one_window = np.repeat(levels, self.samples_per_window // 8)[:, None]
        base = np.tile(one_window, (self.window_count, 1))
        transforms = ((1, 0), (-2, 3), (3, -7), (-4, 11), (5, 17), (-6, -13))
        sources = tuple(
            (scale * base.astype(np.int64) + offset).astype(np.int32)
            for scale, offset in transforms
        )
        result = evaluate_frozen_segments(
            sources[:3], sources[3:], self.samples_per_window
        )
        self.assertEqual(len(result.forward_supported), 1)
        self.assertEqual(result.decision, "reject-development-candidate")

    def test_malformed_frozen_source_sets_are_structural_errors(self):
        sources = self.affine_distinct_segments()
        with self.assertRaises(ValueError):
            evaluate_frozen_segments(sources[:2], sources[3:], self.samples_per_window)
        with self.assertRaises(ValueError):
            evaluate_frozen_segments(
                sources[:3],
                (sources[3][:-1], sources[4], sources[5]),
                self.samples_per_window,
            )

    def test_unrepresentable_integer_polarity_is_a_structural_error(self):
        sources = list(self.affine_distinct_segments())
        sources[0] = sources[0].copy()
        sources[0][0, 0] = np.iinfo(np.int32).min
        with self.assertRaises(ValueError):
            evaluate_frozen_segments(
                tuple(sources[:3]), tuple(sources[3:]), self.samples_per_window
            )


if __name__ == "__main__":
    unittest.main()

