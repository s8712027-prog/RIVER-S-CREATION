"""WITHDRAWN, unexecuted rank-envelope draft.

Do not use this module as a continuation branch.  It duplicates the already
adopted non-exact-cross-source direction after an isolated v2 experiment
mistakenly reintroduced exact ``(C, F)`` recurrence as its validation gate.
The active provisional local-capability reader was never reverted.
"""

from __future__ import annotations

import hashlib
import itertools
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Sequence, Tuple

import numpy as np


BIN_COUNT = 10
LAGS = (1, 2, 3)
WINDOW_COUNT = 64
SAMPLES_PER_WINDOW = 1_600
REQUIRED_SAMPLES = WINDOW_COUNT * SAMPLES_PER_WINDOW
LINKAGE_SHIFT_LIMIT = 31
ADJACENCY_CONTROL_ORDERS = tuple(
    tuple((multiplier * index + offset) % BIN_COUNT for index in range(BIN_COUNT))
    for multiplier in (3, 7)
    for offset in range(BIN_COUNT)
)


def _validate_pcm_dtype(values: np.ndarray) -> None:
    dtype = values.dtype
    supported_integer = np.issubdtype(dtype, np.signedinteger) and dtype.itemsize <= 4
    if dtype != np.dtype(np.float32) and not supported_integer:
        raise ValueError("PCM must be float32 or a signed <=32-bit synthetic integer")


def _doubled_median(values: np.ndarray, axis: int) -> np.ndarray:
    widened = np.asarray(values, dtype=np.float64)
    ordered = np.sort(widened, axis=axis)
    count = ordered.shape[axis]
    lower = (count - 1) // 2
    upper = count // 2
    return np.take(ordered, lower, axis=axis) + np.take(ordered, upper, axis=axis)


@dataclass(frozen=True, order=True)
class LagCurrentVectorA:
    j1: int
    j2: int
    j3: int

    def __neg__(self) -> "LagCurrentVectorA":
        return LagCurrentVectorA(-self.j1, -self.j2, -self.j3)

    def __add__(self, other: "LagCurrentVectorA") -> "LagCurrentVectorA":
        return LagCurrentVectorA(
            self.j1 + other.j1,
            self.j2 + other.j2,
            self.j3 + other.j3,
        )

    @property
    def values(self) -> Tuple[int, int, int]:
        return (self.j1, self.j2, self.j3)

    @property
    def l1(self) -> int:
        return abs(self.j1) + abs(self.j2) + abs(self.j3)

    def dot(self, other: "LagCurrentVectorA") -> int:
        return sum(left * right for left, right in zip(self.values, other.values))


ZERO_VECTOR = LagCurrentVectorA(0, 0, 0)


@dataclass(frozen=True)
class RankEnvelopeOccurrenceA:
    window_index: int
    channel_index: int
    ordinal_profile: Tuple[int, ...]
    current: LagCurrentVectorA
    exact_evidence_token: str


def doubled_mad_envelope(window_pcm: np.ndarray) -> np.ndarray:
    """Return ten robust amplitude-envelope values as float64 [bin, channel]."""
    window = np.asarray(window_pcm)
    if window.ndim != 2 or window.shape[0] != SAMPLES_PER_WINDOW:
        raise ValueError("one window must be [1600, channels]")
    if window.shape[1] <= 0 or not np.all(np.isfinite(window)):
        raise ValueError("window must contain finite channel-preserving PCM")
    _validate_pcm_dtype(window)
    frames_per_bin = SAMPLES_PER_WINDOW // BIN_COUNT
    bins = np.asarray(window, dtype=np.float64).reshape(
        BIN_COUNT, frames_per_bin, window.shape[1]
    )
    centers2 = _doubled_median(bins, axis=1)
    deviations2 = np.abs(2.0 * bins - centers2[:, None, :])
    envelope = _doubled_median(deviations2, axis=1)
    if not np.all(np.isfinite(envelope)):
        raise ValueError("widened rank-envelope arithmetic overflowed")
    return envelope


def ordinal_scores_10(values: Sequence[float]) -> Tuple[int, ...]:
    if len(values) != BIN_COUNT:
        raise ValueError("rank envelope requires exactly ten values")
    array = np.asarray(values, dtype=np.float64)
    if array.shape != (BIN_COUNT,) or not np.all(np.isfinite(array)):
        raise ValueError("rank envelope must be one finite ten-value vector")
    return tuple(
        int(np.count_nonzero(value > array) - np.count_nonzero(value < array))
        for value in array
    )


def lag_current(profile: Sequence[int]) -> LagCurrentVectorA:
    if len(profile) != BIN_COUNT:
        raise ValueError("lag current requires one ten-position ordinal profile")
    q = tuple(int(value) for value in profile)
    if any(value < -9 or value > 9 for value in q) or sum(q) != 0:
        raise ValueError("ordinal profile is outside the frozen tie-safe score domain")
    currents = []
    for lag in LAGS:
        currents.append(sum(
            q[index] * q[index + lag] * (q[index + lag] - q[index])
            for index in range(BIN_COUNT - lag)
        ))
    return LagCurrentVectorA(*currents)


def window_occurrences(window_pcm: np.ndarray, window_index: int) -> Tuple[RankEnvelopeOccurrenceA, ...]:
    envelope = doubled_mad_envelope(window_pcm)
    rows = []
    for channel in range(envelope.shape[1]):
        profile = ordinal_scores_10(envelope[:, channel])
        channel_window = np.ascontiguousarray(np.asarray(window_pcm)[:, channel])
        digest = hashlib.sha256()
        digest.update(str(channel_window.dtype).encode("ascii"))
        digest.update(b"\0")
        digest.update(str(channel_window.shape).encode("ascii"))
        digest.update(b"\0")
        digest.update(channel_window.view(np.uint8).tobytes())
        rows.append(RankEnvelopeOccurrenceA(
            window_index,
            channel,
            profile,
            lag_current(profile),
            digest.hexdigest(),
        ))
    return tuple(rows)


def segment_occurrences(segment_pcm: np.ndarray) -> Tuple[RankEnvelopeOccurrenceA, ...]:
    segment = np.asarray(segment_pcm)
    if segment.ndim != 2 or segment.shape[0] != REQUIRED_SAMPLES:
        raise ValueError("segment must contain exactly 64 complete 1600-sample windows")
    if segment.shape[1] <= 0 or not np.all(np.isfinite(segment)):
        raise ValueError("segment must contain finite channel-preserving PCM")
    _validate_pcm_dtype(segment)
    return tuple(
        item
        for window_index in range(WINDOW_COUNT)
        for item in window_occurrences(
            segment[
                window_index * SAMPLES_PER_WINDOW:(window_index + 1) * SAMPLES_PER_WINDOW
            ],
            window_index,
        )
    )


def source_vector(occurrences: Sequence[RankEnvelopeOccurrenceA]) -> LagCurrentVectorA:
    total = ZERO_VECTOR
    for occurrence in occurrences:
        total = total + occurrence.current
    return total


def reverse_pcm_frames(segment_pcm: np.ndarray) -> np.ndarray:
    segment = np.asarray(segment_pcm)
    if segment.ndim != 2:
        raise ValueError("PCM reversal requires [sample, channel]")
    return np.ascontiguousarray(segment[::-1, :])


def normalized_alignment(template: LagCurrentVectorA, vector: LagCurrentVectorA) -> Fraction:
    denominator = template.l1 * vector.l1
    return Fraction(template.dot(vector), denominator) if denominator else Fraction(0, 1)


def adjacency_control_vector(
    occurrences: Sequence[RankEnvelopeOccurrenceA], order: Sequence[int]
) -> LagCurrentVectorA:
    if tuple(sorted(order)) != tuple(range(BIN_COUNT)):
        raise ValueError("adjacency order must permute all ten positions")
    total = ZERO_VECTOR
    for occurrence in occurrences:
        controlled = tuple(occurrence.ordinal_profile[index] for index in order)
        total = total + lag_current(controlled)
    return total


def linkage_control_vector(
    occurrences: Sequence[RankEnvelopeOccurrenceA], shift: int
) -> LagCurrentVectorA:
    if not 0 < shift < WINDOW_COUNT:
        raise ValueError("linkage shift must be between one and 63")
    by_coordinate = {
        (item.window_index, item.channel_index): item for item in occurrences
    }
    channels = sorted({item.channel_index for item in occurrences})
    expected = {
        (window, channel)
        for window in range(WINDOW_COUNT)
        for channel in channels
    }
    if set(by_coordinate) != expected or len(occurrences) != len(expected):
        raise ValueError("linkage controls require one canonical occurrence grid")
    total = ZERO_VECTOR
    for window in range(WINDOW_COUNT):
        for channel in channels:
            left = by_coordinate[(window, channel)].ordinal_profile[:5]
            right = by_coordinate[((window + shift) % WINDOW_COUNT, channel)].ordinal_profile[5:]
            total = total + lag_current(left + right)
    return total


def strict_current_census(batch_size: int = 65_536) -> Counter[LagCurrentVectorA]:
    if batch_size <= 0:
        raise ValueError("census batch size must be positive")
    census: Counter[LagCurrentVectorA] = Counter()
    permutations = itertools.permutations(range(BIN_COUNT))
    while True:
        batch_rows = list(itertools.islice(permutations, batch_size))
        if not batch_rows:
            break
        ranks = np.asarray(batch_rows, dtype=np.int16)
        q = 2 * ranks - (BIN_COUNT - 1)
        columns = []
        for lag in LAGS:
            left = q[:, :-lag]
            right = q[:, lag:]
            columns.append(np.sum(left * right * (right - left), axis=1, dtype=np.int64))
        vectors = np.stack(columns, axis=1)
        unique, counts = np.unique(vectors, axis=0, return_counts=True)
        census.update({
            LagCurrentVectorA(int(row[0]), int(row[1]), int(row[2])): int(count)
            for row, count in zip(unique, counts)
        })
    return census


def _polarity_invert(segment: np.ndarray) -> np.ndarray:
    if segment.dtype == np.float32:
        return np.ascontiguousarray(-segment)
    limits = np.iinfo(segment.dtype)
    widened = -segment.astype(np.int64)
    if np.any(widened < limits.min) or np.any(widened > limits.max):
        raise ValueError("synthetic integer PCM cannot be polarity-inverted in its dtype")
    return np.ascontiguousarray(widened.astype(segment.dtype))


@dataclass(frozen=True)
class IrreversibilityDevelopmentDecisionA:
    decision: str
    formation_vectors: Tuple[LagCurrentVectorA, LagCurrentVectorA, LagCurrentVectorA]
    template: LagCurrentVectorA
    formation_leave_one_out_dots: Tuple[int, int, int]
    heldout_vectors: Tuple[LagCurrentVectorA, LagCurrentVectorA, LagCurrentVectorA]
    forward_alignments: Tuple[Fraction, Fraction, Fraction]
    reverse_alignments: Tuple[Fraction, Fraction, Fraction]
    forward_aggregate: Fraction
    reverse_aggregate: Fraction
    control_aggregates: Tuple[Tuple[str, Fraction], ...]
    raw_reversal_identity_valid: bool
    pcm_invariants_valid: bool
    exact_evidence_disjoint: bool
    reason: str


def _evidence_disjoint(
    sources: Sequence[Sequence[RankEnvelopeOccurrenceA]],
) -> bool:
    evidence = [
        {item.exact_evidence_token for item in source} for source in sources
    ]
    return all(
        left.isdisjoint(right)
        for index, left in enumerate(evidence)
        for right in evidence[index + 1:]
    )


def _raw_reverse_identity(
    heldout: Sequence[Sequence[RankEnvelopeOccurrenceA]],
    reversed_heldout: Sequence[Sequence[RankEnvelopeOccurrenceA]],
) -> bool:
    for forward_source, reverse_source in zip(heldout, reversed_heldout):
        reverse_by_coordinate = {
            (item.window_index, item.channel_index): item for item in reverse_source
        }
        for item in forward_source:
            mirror = reverse_by_coordinate.get(
                (WINDOW_COUNT - 1 - item.window_index, item.channel_index)
            )
            if (
                mirror is None
                or mirror.ordinal_profile != tuple(reversed(item.ordinal_profile))
                or mirror.current != -item.current
            ):
                return False
    return True


def _pcm_invariants(
    segments: Sequence[np.ndarray],
    sources: Sequence[Sequence[RankEnvelopeOccurrenceA]],
) -> bool:
    for segment, source in zip(segments, sources):
        polarity = segment_occurrences(_polarity_invert(segment))
        if any(left.current != right.current for left, right in zip(source, polarity)):
            return False
        permuted = segment_occurrences(np.ascontiguousarray(segment[:, ::-1]))
        channel_count = segment.shape[1]
        permuted_map = {
            (item.window_index, item.channel_index): item for item in permuted
        }
        if any(
            permuted_map[
                (item.window_index, channel_count - 1 - item.channel_index)
            ].current != item.current
            for item in source
        ):
            return False
    return True


def evaluate_frozen_segments(
    formation_segments: Sequence[np.ndarray],
    heldout_segments: Sequence[np.ndarray],
) -> IrreversibilityDevelopmentDecisionA:
    """Fail-closed synthetic evaluator over raw 3+3 frozen segments."""
    frozen_orders = tuple(
        tuple((multiplier * index + offset) % 10 for index in range(10))
        for multiplier in (3, 7)
        for offset in range(10)
    )
    if (
        BIN_COUNT != 10
        or LAGS != (1, 2, 3)
        or WINDOW_COUNT != 64
        or SAMPLES_PER_WINDOW != 1_600
        or LINKAGE_SHIFT_LIMIT != 31
        or ADJACENCY_CONTROL_ORDERS != frozen_orders
    ):
        raise RuntimeError("the frozen irreversibility manifest was rebound")
    if len(formation_segments) != 3 or len(heldout_segments) != 3:
        raise ValueError("evaluation requires exactly three formation and three heldout sources")
    all_segments = tuple(np.asarray(item) for item in (*formation_segments, *heldout_segments))
    if len({item.shape for item in all_segments}) != 1:
        raise ValueError("all six raw segments require one compatible frozen shape")
    formation_occurrences = tuple(segment_occurrences(item) for item in formation_segments)
    heldout_occurrences = tuple(segment_occurrences(item) for item in heldout_segments)
    reversed_occurrences = tuple(
        segment_occurrences(reverse_pcm_frames(item)) for item in heldout_segments
    )
    formation_vectors = tuple(source_vector(source) for source in formation_occurrences)
    heldout_vectors = tuple(source_vector(source) for source in heldout_occurrences)
    reversed_vectors = tuple(source_vector(source) for source in reversed_occurrences)
    template = formation_vectors[0] + formation_vectors[1] + formation_vectors[2]
    leave_one_out = tuple(
        formation_vectors[index].dot(
            formation_vectors[(index + 1) % 3] + formation_vectors[(index + 2) % 3]
        )
        for index in range(3)
    )
    forward_alignments = tuple(normalized_alignment(template, vector) for vector in heldout_vectors)
    reverse_alignments = tuple(normalized_alignment(template, vector) for vector in reversed_vectors)
    forward_aggregate = sum(forward_alignments, Fraction(0, 1))
    reverse_aggregate = sum(reverse_alignments, Fraction(0, 1))

    control_aggregates = []
    for (multiplier, offset), order in zip(
        itertools.product((3, 7), range(10)), frozen_orders
    ):
        controlled = tuple(
            adjacency_control_vector(source, order) for source in heldout_occurrences
        )
        aggregate = sum(
            (normalized_alignment(template, vector) for vector in controlled),
            Fraction(0, 1),
        )
        control_aggregates.append((f"adjacency:a{multiplier}-b{offset}", aggregate))
    for shift in range(1, 32):
        controlled = tuple(
            linkage_control_vector(source, shift) for source in heldout_occurrences
        )
        aggregate = sum(
            (normalized_alignment(template, vector) for vector in controlled),
            Fraction(0, 1),
        )
        control_aggregates.append((f"half-linkage:shift-{shift:02d}", aggregate))
    if len(control_aggregates) != 51:
        raise AssertionError("complete 51-control manifest was not constructed")

    raw_identity = _raw_reverse_identity(heldout_occurrences, reversed_occurrences)
    source_reverse_identity = all(
        reverse == -forward for forward, reverse in zip(heldout_vectors, reversed_vectors)
    )
    invariants = _pcm_invariants(all_segments, (*formation_occurrences, *heldout_occurrences))
    evidence = _evidence_disjoint((*formation_occurrences, *heldout_occurrences))
    formation_coherent = template != ZERO_VECTOR and all(value > 0 for value in leave_one_out)
    passed = (
        formation_coherent
        and all(value > 0 for value in forward_alignments)
        and all(forward > reverse for forward, reverse in zip(forward_alignments, reverse_alignments))
        and forward_aggregate > reverse_aggregate
        and all(forward_aggregate > value for _, value in control_aggregates)
        and raw_identity
        and source_reverse_identity
        and invariants
        and evidence
    )
    return IrreversibilityDevelopmentDecisionA(
        "retain-development-candidate" if passed else "reject-development-candidate",
        formation_vectors,  # type: ignore[arg-type]
        template,
        leave_one_out,  # type: ignore[arg-type]
        heldout_vectors,  # type: ignore[arg-type]
        forward_alignments,  # type: ignore[arg-type]
        reverse_alignments,  # type: ignore[arg-type]
        forward_aggregate,
        reverse_aggregate,
        tuple(control_aggregates),
        raw_identity and source_reverse_identity,
        invariants,
        evidence,
        (
            "formation and all heldout sources aligned and cleared every frozen control"
            if passed
            else "formation coherence, heldout alignment, or a mandatory control/invariant failed"
        ),
    )

