"""Synthetic-first local ordinal parity moments with exact reversal law."""

from __future__ import annotations

import hashlib
import itertools
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence, Tuple

import numpy as np


MICROBIN_COUNT = 8
ROUGHNESS_COUNT = 7
FROZEN_WINDOW_COUNT = 64
LINKAGE_SHIFT_LIMIT = 31
POSITION_WEIGHTS = tuple(range(-3, 4))
EVEN_WEIGHTS = tuple(value * value - 4 for value in POSITION_WEIGHTS)
ADJACENCY_CONTROL_ORDERS = tuple(
    tuple((multiplier * index + offset) % ROUGHNESS_COUNT for index in range(ROUGHNESS_COUNT))
    for multiplier in (2, 3, 4, 5)
    for offset in range(ROUGHNESS_COUNT)
)


def _sign(value: float | int) -> int:
    return 1 if value > 0 else -1 if value < 0 else 0


def _validate_pcm_dtype(values: np.ndarray) -> None:
    dtype = values.dtype
    supported_integer = np.issubdtype(dtype, np.signedinteger) and dtype.itemsize <= 4
    if dtype != np.dtype(np.float32) and not supported_integer:
        raise ValueError("PCM must be float32 neutral data or a signed <=32-bit synthetic integer")


@dataclass(frozen=True, order=True)
class OrdinalMomentKeyA:
    carrier_even: int
    arrow_odd: int

    @property
    def oriented(self) -> bool:
        return self.arrow_odd != 0

    def reversed(self) -> "OrdinalMomentKeyA":
        return OrdinalMomentKeyA(self.carrier_even, -self.arrow_odd)


@dataclass(frozen=True)
class OrdinalMomentOccurrenceA:
    window_index: int
    channel_index: int
    roughness_magnitudes: Tuple[float, ...]
    key: OrdinalMomentKeyA
    exact_evidence_token: str


def doubled_microbin_medians(window_pcm: np.ndarray) -> np.ndarray:
    """Return eight mirror-closed twice-medians as float64 [bin, channel]."""
    window = np.asarray(window_pcm)
    if window.ndim != 2 or window.shape[0] < MICROBIN_COUNT:
        raise ValueError("PCM window must be [frames, channels] with at least eight frames")
    if window.shape[0] % MICROBIN_COUNT:
        raise ValueError("PCM window frame count must divide exactly into eight microbins")
    if window.shape[1] <= 0 or not np.all(np.isfinite(window)):
        raise ValueError("PCM window must contain finite channel-preserving samples")
    _validate_pcm_dtype(window)
    frames_per_bin = window.shape[0] // MICROBIN_COUNT
    bins = np.asarray(window, dtype=np.float64).reshape(
        MICROBIN_COUNT, frames_per_bin, window.shape[1]
    )
    ordered = np.sort(bins, axis=1)
    lower = (frames_per_bin - 1) // 2
    upper = frames_per_bin // 2
    result = ordered[:, lower, :] + ordered[:, upper, :]
    if not np.all(np.isfinite(result)):
        raise ValueError("widened doubled median overflowed")
    return result


def roughness_magnitudes(window_pcm: np.ndarray) -> np.ndarray:
    medians = doubled_microbin_medians(window_pcm)
    result = np.abs(np.diff(medians, axis=0))
    if not np.all(np.isfinite(result)):
        raise ValueError("roughness magnitude overflowed")
    return result


def ordinal_scores(values: Sequence[float]) -> Tuple[int, ...]:
    if len(values) != ROUGHNESS_COUNT:
        raise ValueError("ordinal profile requires exactly seven roughness values")
    array = np.asarray(values, dtype=np.float64)
    if array.shape != (ROUGHNESS_COUNT,) or not np.all(np.isfinite(array)):
        raise ValueError("roughness profile must be one finite seven-value vector")
    return tuple(
        int(np.count_nonzero(value > array) - np.count_nonzero(value < array))
        for value in array
    )


def parity_moment_key(values: Sequence[float]) -> OrdinalMomentKeyA:
    scores = ordinal_scores(values)
    assert sum(scores) == 0
    carrier = sum(weight * score for weight, score in zip(EVEN_WEIGHTS, scores))
    arrow = sum(weight * score for weight, score in zip(POSITION_WEIGHTS, scores))
    return OrdinalMomentKeyA(carrier, arrow)


def window_channel_keys(window_pcm: np.ndarray) -> Tuple[OrdinalMomentKeyA, ...]:
    roughness = roughness_magnitudes(window_pcm)
    return tuple(parity_moment_key(roughness[:, channel]) for channel in range(roughness.shape[1]))


def exact_channel_window_token(channel_window: np.ndarray) -> str:
    values = np.ascontiguousarray(channel_window)
    digest = hashlib.sha256()
    digest.update(str(values.dtype).encode("ascii"))
    digest.update(b"\0")
    digest.update(str(values.shape).encode("ascii"))
    digest.update(b"\0")
    digest.update(values.view(np.uint8).tobytes())
    return digest.hexdigest()


def segment_occurrences(
    segment_pcm: np.ndarray, samples_per_window: int, window_count: int = FROZEN_WINDOW_COUNT
) -> Tuple[OrdinalMomentOccurrenceA, ...]:
    segment = np.asarray(segment_pcm)
    if samples_per_window <= 0 or window_count <= 0:
        raise ValueError("window geometry must be positive")
    if segment.ndim != 2 or segment.shape[0] != samples_per_window * window_count:
        raise ValueError("segment must contain exactly the frozen number of complete windows")
    if samples_per_window % MICROBIN_COUNT:
        raise ValueError("samples per window must divide exactly into eight microbins")
    if segment.shape[1] <= 0 or not np.all(np.isfinite(segment)):
        raise ValueError("segment must contain finite channel-preserving PCM")
    _validate_pcm_dtype(segment)
    occurrences = []
    for window_index in range(window_count):
        start = window_index * samples_per_window
        window = segment[start:start + samples_per_window]
        roughness = roughness_magnitudes(window)
        for channel in range(segment.shape[1]):
            profile = tuple(float(value) for value in roughness[:, channel])
            occurrences.append(OrdinalMomentOccurrenceA(
                window_index,
                channel,
                profile,
                parity_moment_key(profile),
                exact_channel_window_token(window[:, channel]),
            ))
    return tuple(occurrences)


def reverse_pcm_frames(segment_pcm: np.ndarray) -> np.ndarray:
    segment = np.asarray(segment_pcm)
    if segment.ndim != 2:
        raise ValueError("PCM reversal must preserve a [frames, channels] array")
    return np.ascontiguousarray(segment[::-1, :])


def adjacency_control_key(
    occurrence: OrdinalMomentOccurrenceA, order: Sequence[int]
) -> OrdinalMomentKeyA:
    if tuple(sorted(order)) != tuple(range(ROUGHNESS_COUNT)):
        raise ValueError("adjacency control order must permute all seven positions")
    values = tuple(occurrence.roughness_magnitudes[index] for index in order)
    return parity_moment_key(values)


def adjacency_control_key_sets(
    occurrences: Sequence[OrdinalMomentOccurrenceA],
) -> Mapping[str, frozenset[OrdinalMomentKeyA]]:
    return {
        f"a{multiplier}-b{offset}": frozenset(
            adjacency_control_key(occurrence, order) for occurrence in occurrences
        )
        for (multiplier, offset), order in zip(
            itertools.product((2, 3, 4, 5), range(ROUGHNESS_COUNT)),
            ADJACENCY_CONTROL_ORDERS,
        )
    }


def linkage_control_keys(
    occurrences: Sequence[OrdinalMomentOccurrenceA], shift: int
) -> Tuple[OrdinalMomentKeyA, ...]:
    count = len(occurrences)
    if count < 2 or not 0 < shift < count:
        raise ValueError("linkage shift must be positive and smaller than occurrence count")
    return tuple(
        OrdinalMomentKeyA(
            occurrence.key.carrier_even,
            occurrences[(index + shift) % count].key.arrow_odd,
        )
        for index, occurrence in enumerate(occurrences)
    )


def linkage_control_key_sets(
    occurrences: Sequence[OrdinalMomentOccurrenceA], shift_limit: int = LINKAGE_SHIFT_LIMIT
) -> Mapping[int, frozenset[OrdinalMomentKeyA]]:
    if len(occurrences) < 2:
        raise ValueError("linkage controls require at least two occurrences")
    return {
        shift: frozenset(linkage_control_keys(occurrences, shift))
        for shift in range(1, min(shift_limit, len(occurrences) - 1) + 1)
    }


def strict_rank_key_census() -> Counter[OrdinalMomentKeyA]:
    census: Counter[OrdinalMomentKeyA] = Counter()
    for ranks in itertools.permutations(range(ROUGHNESS_COUNT)):
        scores = tuple(2 * rank - (ROUGHNESS_COUNT - 1) for rank in ranks)
        carrier = sum(weight * score for weight, score in zip(EVEN_WEIGHTS, scores))
        arrow = sum(weight * score for weight, score in zip(POSITION_WEIGHTS, scores))
        census[OrdinalMomentKeyA(carrier, arrow)] += 1
    return census


def _occurrence_sources(
    sources: Sequence[Sequence[OrdinalMomentOccurrenceA]],
    window_count: int,
) -> Tuple[Tuple[OrdinalMomentOccurrenceA, ...], ...]:
    if len(sources) != 3:
        raise ValueError("frozen development comparison requires exactly three sources")
    normalized = tuple(tuple(source) for source in sources)
    channel_counts = []
    for source in normalized:
        if not source:
            raise ValueError("every frozen source must contain occurrences")
        coordinates = {(item.window_index, item.channel_index) for item in source}
        channels = {item.channel_index for item in source}
        if channels != set(range(len(channels))):
            raise ValueError("source channels must be consecutive and zero-based")
        expected = {
            (window, channel)
            for window in range(window_count)
            for channel in channels
        }
        if coordinates != expected or len(source) != len(expected):
            raise ValueError("source must contain one occurrence per frozen window and channel")
        for item in source:
            if len(item.roughness_magnitudes) != ROUGHNESS_COUNT:
                raise ValueError("occurrence roughness profile is incomplete")
            if item.key != parity_moment_key(item.roughness_magnitudes):
                raise ValueError("occurrence key does not reproduce from its roughness evidence")
            if len(item.exact_evidence_token) != 64 or any(
                character not in "0123456789abcdef" for character in item.exact_evidence_token
            ):
                raise ValueError("occurrence exact evidence token is invalid")
        channel_counts.append(len(channels))
    if len(set(channel_counts)) != 1:
        raise ValueError("all frozen sources must have one compatible channel count")
    return tuple(
        tuple(sorted(source, key=lambda item: (item.window_index, item.channel_index)))
        for source in normalized
    )


def _source_key_sets(
    sources: Sequence[Sequence[OrdinalMomentOccurrenceA]],
) -> Tuple[frozenset[OrdinalMomentKeyA], ...]:
    return tuple(frozenset(item.key for item in source) for source in sources)


def _incidence_at_least_two(
    candidates: Iterable[OrdinalMomentKeyA], sources: Sequence[frozenset[OrdinalMomentKeyA]]
) -> frozenset[OrdinalMomentKeyA]:
    return frozenset(
        key for key in candidates if sum(key in source for source in sources) >= 2
    )


@dataclass(frozen=True)
class OrdinalMomentDevelopmentDecisionA:
    decision: str
    formation_dictionary: frozenset[OrdinalMomentKeyA]
    forward_supported: frozenset[OrdinalMomentKeyA]
    reverse_supported: frozenset[OrdinalMomentKeyA]
    per_heldout_forward: Tuple[int, int, int]
    per_heldout_reverse: Tuple[int, int, int]
    formation_three_of_three: frozenset[OrdinalMomentKeyA]
    heldout_three_of_three: frozenset[OrdinalMomentKeyA]
    formation_occurrence_capacity: Tuple[int, int, int]
    heldout_occurrence_capacity: Tuple[int, int, int]
    formation_distinct_key_counts: Tuple[int, int, int]
    heldout_distinct_key_counts: Tuple[int, int, int]
    formation_zero_arrow_counts: Tuple[int, int, int]
    heldout_zero_arrow_counts: Tuple[int, int, int]
    control_support_counts: Tuple[Tuple[str, int], ...]
    raw_reversal_identity_valid: bool
    pcm_invariants_valid: bool
    exact_evidence_disjoint: bool
    reason: str


def _polarity_invert_pcm(segment_pcm: np.ndarray) -> np.ndarray:
    segment = np.asarray(segment_pcm)
    _validate_pcm_dtype(segment)
    if segment.dtype == np.dtype(np.float32):
        return np.ascontiguousarray(-segment)
    limits = np.iinfo(segment.dtype)
    widened = -segment.astype(np.int64)
    if np.any(widened < limits.min) or np.any(widened > limits.max):
        raise ValueError("synthetic integer PCM cannot be polarity-inverted in its dtype")
    return np.ascontiguousarray(widened.astype(segment.dtype))


def _pcm_invariant_identity(
    segments: Sequence[np.ndarray],
    baseline_sources: Sequence[Sequence[OrdinalMomentOccurrenceA]],
    samples_per_window: int,
    window_count: int,
) -> bool:
    for segment, baseline in zip(segments, baseline_sources):
        polarity = segment_occurrences(
            _polarity_invert_pcm(segment), samples_per_window, window_count
        )
        polarity_by_coordinate = {
            (item.window_index, item.channel_index): item.key for item in polarity
        }
        if any(
            polarity_by_coordinate.get((item.window_index, item.channel_index)) != item.key
            for item in baseline
        ):
            return False

        channel_count = segment.shape[1]
        permuted = segment_occurrences(
            np.ascontiguousarray(segment[:, ::-1]),
            samples_per_window,
            window_count,
        )
        permuted_by_coordinate = {
            (item.window_index, item.channel_index): item.key for item in permuted
        }
        if any(
            permuted_by_coordinate.get(
                (item.window_index, channel_count - 1 - item.channel_index)
            ) != item.key
            for item in baseline
        ):
            return False
    return True


def _raw_reverse_identity(
    heldout: Sequence[Sequence[OrdinalMomentOccurrenceA]],
    reversed_heldout: Sequence[Sequence[OrdinalMomentOccurrenceA]],
    window_count: int,
) -> bool:
    for forward_source, reverse_source in zip(heldout, reversed_heldout):
        reverse_by_coordinate = {
            (item.window_index, item.channel_index): item for item in reverse_source
        }
        for item in forward_source:
            mirror = reverse_by_coordinate.get(
                (window_count - 1 - item.window_index, item.channel_index)
            )
            if mirror is None or mirror.key != item.key.reversed():
                return False
    return True


def _supported_evidence_disjoint(
    supported: Iterable[OrdinalMomentKeyA],
    formation: Sequence[Sequence[OrdinalMomentOccurrenceA]],
    heldout: Sequence[Sequence[OrdinalMomentOccurrenceA]],
) -> bool:
    for key in supported:
        evidence_by_source = []
        for group in (formation, heldout):
            supporting = []
            for source in group:
                evidence = {
                    item.exact_evidence_token for item in source if item.key == key
                }
                if evidence:
                    supporting.append(evidence)
            if len(supporting) < 2:
                return False
            evidence_by_source.extend(supporting)
        for index, evidence in enumerate(evidence_by_source):
            if any(evidence & other for other in evidence_by_source[index + 1:]):
                return False
    return True


def evaluate_frozen_segments(
    formation_segments: Sequence[np.ndarray],
    heldout_segments: Sequence[np.ndarray],
    samples_per_window: int,
) -> OrdinalMomentDevelopmentDecisionA:
    """Synthetic-only fail-closed evaluator; reverse and controls are internal."""
    frozen_window_count = 64
    frozen_linkage_shift_limit = 31
    frozen_position_weights = tuple(range(-3, 4))
    frozen_even_weights = tuple(value * value - 4 for value in frozen_position_weights)
    frozen_adjacency_orders = tuple(
        tuple((multiplier * index + offset) % 7 for index in range(7))
        for multiplier in (2, 3, 4, 5)
        for offset in range(7)
    )
    if (
        MICROBIN_COUNT != 8
        or ROUGHNESS_COUNT != 7
        or FROZEN_WINDOW_COUNT != frozen_window_count
        or LINKAGE_SHIFT_LIMIT != frozen_linkage_shift_limit
        or POSITION_WEIGHTS != frozen_position_weights
        or EVEN_WEIGHTS != frozen_even_weights
        or ADJACENCY_CONTROL_ORDERS != frozen_adjacency_orders
    ):
        raise RuntimeError("the frozen ordinal-moment manifest was rebound")
    if len(formation_segments) != 3 or len(heldout_segments) != 3:
        raise ValueError("frozen evaluation requires three formation and three heldout segments")
    all_segments = tuple(np.asarray(item) for item in (*formation_segments, *heldout_segments))
    shapes = {item.shape for item in all_segments}
    if len(shapes) != 1:
        raise ValueError("all frozen source segments must have one compatible shape")

    formation_occurrences = _occurrence_sources(
        tuple(
            segment_occurrences(item, samples_per_window, frozen_window_count)
            for item in formation_segments
        ),
        frozen_window_count,
    )
    heldout_occurrences = _occurrence_sources(
        tuple(
            segment_occurrences(item, samples_per_window, frozen_window_count)
            for item in heldout_segments
        ),
        frozen_window_count,
    )
    reversed_occurrences = _occurrence_sources(
        tuple(
            segment_occurrences(
                reverse_pcm_frames(item), samples_per_window, frozen_window_count
            )
            for item in heldout_segments
        ),
        frozen_window_count,
    )
    pcm_invariants_valid = _pcm_invariant_identity(
        all_segments,
        (*formation_occurrences, *heldout_occurrences),
        samples_per_window,
        frozen_window_count,
    )
    channel_counts = {
        len({item.channel_index for item in group[0]})
        for group in (formation_occurrences, heldout_occurrences, reversed_occurrences)
    }
    if len(channel_counts) != 1:
        raise ValueError("formation, heldout, and reverse channel counts must match")

    formation = _source_key_sets(formation_occurrences)
    heldout = _source_key_sets(heldout_occurrences)
    reversed_heldout = _source_key_sets(reversed_occurrences)
    dictionary = _incidence_at_least_two(
        (key for source in formation for key in source if key.oriented), formation
    )
    forward = _incidence_at_least_two(dictionary, heldout)
    reverse = _incidence_at_least_two(dictionary, reversed_heldout)
    per_forward = tuple(len(dictionary & source) for source in heldout)
    per_reverse = tuple(len(dictionary & source) for source in reversed_heldout)
    formation_three_of_three = frozenset(
        key for key in dictionary if all(key in source for source in formation)
    )
    heldout_three_of_three = frozenset(
        key for key in dictionary if all(key in source for source in heldout)
    )
    formation_capacity = tuple(len(source) for source in formation_occurrences)
    heldout_capacity = tuple(len(source) for source in heldout_occurrences)
    formation_distinct = tuple(len(source) for source in formation)
    heldout_distinct = tuple(len(source) for source in heldout)
    formation_zero_arrow = tuple(
        sum(not item.key.oriented for item in source) for source in formation_occurrences
    )
    heldout_zero_arrow = tuple(
        sum(not item.key.oriented for item in source) for source in heldout_occurrences
    )

    if (
        len(frozen_adjacency_orders) != 28
        or len(set(frozen_adjacency_orders)) != 28
        or any(tuple(sorted(order)) != tuple(range(7)) for order in frozen_adjacency_orders)
        or any(
            abs(right - left) == 1
            for order in frozen_adjacency_orders
            for left, right in zip(order, order[1:])
        )
    ):
        raise AssertionError("the frozen adjacency-control manifest is invalid")

    control_counts = []
    for (multiplier, offset), order in zip(
        itertools.product((2, 3, 4, 5), range(7)),
        frozen_adjacency_orders,
    ):
        source_sets = tuple(
            frozenset(adjacency_control_key(item, order) for item in source)
            for source in heldout_occurrences
        )
        supported = _incidence_at_least_two(dictionary, source_sets)
        control_counts.append((f"adjacency:a{multiplier}-b{offset}", len(supported)))

    occurrence_count = len(heldout_occurrences[0])
    if occurrence_count <= frozen_linkage_shift_limit:
        raise ValueError("frozen linkage controls require at least 32 occurrences per source")
    for shift in range(1, frozen_linkage_shift_limit + 1):
        controlled_sources = tuple(
            linkage_control_keys(source, shift) for source in heldout_occurrences
        )
        for source, controlled in zip(heldout_occurrences, controlled_sources):
            if (
                len(controlled) != len(source)
                or Counter(key.carrier_even for key in controlled)
                != Counter(item.key.carrier_even for item in source)
                or Counter(key.arrow_odd for key in controlled)
                != Counter(item.key.arrow_odd for item in source)
            ):
                raise AssertionError("a linkage control changed capacity or marginals")
        source_sets = tuple(frozenset(controlled) for controlled in controlled_sources)
        supported = _incidence_at_least_two(dictionary, source_sets)
        control_counts.append((f"linkage:shift-{shift:02d}", len(supported)))

    if len(control_counts) != 59:
        raise AssertionError("the complete frozen control manifest was not constructed")
    raw_identity_valid = _raw_reverse_identity(
        heldout_occurrences, reversed_occurrences, frozen_window_count
    )
    evidence_disjoint = _supported_evidence_disjoint(
        forward, formation_occurrences, heldout_occurrences
    )
    control_max = max(count for _, count in control_counts)
    passed = (
        len(forward) >= 2
        and len(forward) > len(reverse)
        and len(forward) > control_max
        and all(after > before for after, before in zip(per_forward, per_reverse))
        and evidence_disjoint
        and raw_identity_valid
        and pcm_invariants_valid
    )
    decision = "retain-development-candidate" if passed else "reject-development-candidate"
    reason = (
        "at least two source-recurrent oriented moment keys cleared every frozen control"
        if passed
        else "forward source incidence or a mandatory invariant did not strictly clear the frozen rule"
    )
    return OrdinalMomentDevelopmentDecisionA(
        decision,
        dictionary,
        forward,
        reverse,
        per_forward,  # type: ignore[arg-type]
        per_reverse,  # type: ignore[arg-type]
        formation_three_of_three,
        heldout_three_of_three,
        formation_capacity,  # type: ignore[arg-type]
        heldout_capacity,  # type: ignore[arg-type]
        formation_distinct,  # type: ignore[arg-type]
        heldout_distinct,  # type: ignore[arg-type]
        formation_zero_arrow,  # type: ignore[arg-type]
        heldout_zero_arrow,  # type: ignore[arg-type]
        tuple(control_counts),
        raw_identity_valid,
        pcm_invariants_valid,
        evidence_disjoint,
        reason,
    )

