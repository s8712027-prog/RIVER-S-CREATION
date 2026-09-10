"""Curve OS Guard: dependency-free, offline-first evaluation core.

The module deliberately separates data trust, process compliance, and outcome
risk. Demonstration records are never used to state a production failure risk.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_time(value: str) -> datetime:
    clean = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(clean)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def load_curve_csv(path: Path) -> tuple[list[datetime], list[float], list[float | None]]:
    """Read the customer interchange contract: timestamp,temp_c[,setpoint_c]."""
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"timestamp", "temp_c"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("CSV 必須包含欄位：timestamp,temp_c；setpoint_c 為選填。")
        rows = list(reader)
    if len(rows) < 24:
        raise ValueError("曲線至少需要 24 個採樣點，才可評估。")
    times, temps, setpoints = [], [], []
    for index, row in enumerate(rows, start=2):
        try:
            times.append(parse_time(row["timestamp"]))
            temps.append(float(row["temp_c"]))
            setpoints.append(float(row["setpoint_c"]) if row.get("setpoint_c") else None)
        except (ValueError, TypeError) as error:
            raise ValueError(f"第 {index} 列無法讀取：{error}") from error
    paired = sorted(zip(times, temps, setpoints), key=lambda item: item[0])
    return [x[0] for x in paired], [x[1] for x in paired], [x[2] for x in paired]


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def safe_stdev(values: list[float]) -> float:
    return statistics.stdev(values) if len(values) > 1 else 0.0


def robust_std(values: list[float]) -> float:
    ordered = sorted(values)
    if len(ordered) < 4:
        return safe_stdev(values)
    q1, q3 = statistics.quantiles(ordered, n=4, method="inclusive")[0], statistics.quantiles(ordered, n=4, method="inclusive")[2]
    return (q3 - q1) / 1.349


def score_data_quality(times: list[datetime], temps: list[float], policy: dict[str, Any]) -> dict[str, Any]:
    deltas = [(right - left).total_seconds() for left, right in zip(times, times[1:])]
    non_increasing = sum(1 for value in deltas if value <= 0)
    nominal = statistics.median(deltas) if deltas else 0.0
    jitter = safe_stdev(deltas) / nominal if nominal else 1.0
    # First differences contain intentional heating/cooling slope.  Use the
    # second difference to isolate point-to-point jitter from a valid ramp.
    curvature = [right - 2 * middle + left for left, middle, right in zip(temps, temps[1:], temps[2:])]
    noise = robust_std(curvature)
    plausible = [policy["plausible_temp_c"][0] <= x <= policy["plausible_temp_c"][1] for x in temps]
    scores = {
        "completeness": 1.0,
        "sampling_regularity": clamp(1 - jitter / policy["max_sampling_jitter_ratio"]),
        "sensor_plausibility": sum(plausible) / len(plausible),
        "noise_stability": clamp(1 - noise / policy["max_point_noise_c"]),
    }
    weights = policy["data_quality_weights"]
    score = sum(scores[name] * weights[name] for name in weights)
    reasons = []
    if non_increasing:
        reasons.append("timestamp 不可重複或倒序")
    if scores["sampling_regularity"] < 0.7:
        reasons.append("取樣間隔不穩定")
    if scores["sensor_plausibility"] < 1.0:
        reasons.append("溫度超出感測器合理範圍")
    if scores["noise_stability"] < 0.7:
        reasons.append("點對點雜訊過高")
    return {
        "score": round(score, 3), "pass": not reasons and score >= policy["data_quality_gate"],
        "components": {key: round(value, 3) for key, value in scores.items()},
        "noise_est_c": round(noise, 3), "sampling_jitter_ratio": round(jitter, 3), "fail_reasons": reasons,
    }


def split_phases(values: list[float]) -> dict[str, list[float]]:
    """Temporary deterministic segmentation; deployment replaces this with recipe events."""
    one, two = len(values) // 3, len(values) * 2 // 3
    return {"heating": values[:one], "soaking": values[one:two], "cooling": values[two:]}


def slope_per_min(values: list[float], times: list[datetime]) -> float:
    if len(values) < 2:
        return 0.0
    duration = (times[-1] - times[0]).total_seconds() / 60
    return (values[-1] - values[0]) / duration if duration else 0.0


def feature_margin(value: float, low: float | None, high: float | None, tolerance: float) -> float:
    violation = max(0.0, (low - value) if low is not None else 0.0, (value - high) if high is not None else 0.0)
    return clamp(1 - violation / tolerance) if tolerance else float(violation == 0)


def extract_features(times: list[datetime], temps: list[float], recipe: dict[str, Any]) -> dict[str, float]:
    phases = split_phases(temps)
    indexes = [len(temps) // 3, len(temps) * 2 // 3]
    heating_times, soaking_times, cooling_times = times[:indexes[0]], times[indexes[0]:indexes[1]], times[indexes[1]:]
    soak = phases["soaking"]
    setpoint = recipe["soaking_setpoint_c"]
    return {
        "heating_rate_c_per_min": round(slope_per_min(phases["heating"], heating_times), 3),
        "soaking_mean_error_c": round(statistics.mean(soak) - setpoint, 3),
        "soaking_stability_c": round(robust_std(soak), 3),
        "soaking_duration_min": round((soaking_times[-1] - soaking_times[0]).total_seconds() / 60, 3),
        "cooling_rate_c_per_min": round(slope_per_min(phases["cooling"], cooling_times), 3),
        # As above, a steady ramp is process behaviour, not residual noise.
        "residual_energy_c": round(robust_std([right - 2 * middle + left for left, middle, right in zip(temps, temps[1:], temps[2:])]), 3),
    }


def score_process(features: dict[str, float], recipe: dict[str, Any]) -> dict[str, Any]:
    checks = recipe["acceptance_limits"]
    margins = {
        name: feature_margin(features[name], rule.get("min"), rule.get("max"), rule["tolerance"])
        for name, rule in checks.items()
    }
    weights = recipe["process_quality_weights"]
    score = sum(margins[name] * weights[name] for name in weights)
    failed = [name for name, margin in margins.items() if margin < 1.0]
    return {"score": round(score, 3), "pass": not failed and score >= recipe["process_quality_gate"], "components": {key: round(value, 3) for key, value in margins.items()}, "failed_features": failed}


def resample(values: list[float], count: int = 16) -> list[float]:
    if len(values) == 1:
        return values * count
    output = []
    for i in range(count):
        position = i * (len(values) - 1) / (count - 1)
        left, right = int(position), min(int(position) + 1, len(values) - 1)
        output.append(values[left] + (values[right] - values[left]) * (position - left))
    return output


def l2_normalize(values: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in values))
    return [round(value / norm, 8) for value in values] if norm else values


def make_fingerprint(temps: list[float], features: dict[str, float]) -> list[float]:
    shape = []
    for phase in split_phases(temps).values():
        mean, scale = statistics.mean(phase), safe_stdev(phase) or 1.0
        shape.extend((x - mean) / scale for x in resample(phase))
    feature_vector = [features[key] / scale for key, scale in {
        "heating_rate_c_per_min": 4, "soaking_mean_error_c": 20, "soaking_stability_c": 10,
        "soaking_duration_min": 20, "cooling_rate_c_per_min": 4, "residual_energy_c": 10,
    }.items()]
    return l2_normalize(shape + feature_vector)


def cosine_similarity(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def find_neighbors(fingerprint: list[float], history: list[dict[str, Any]], coil_id: str, recipe_family: str) -> list[dict[str, Any]]:
    eligible = [row for row in history if row.get("coil_id") != coil_id and not row.get("synthetic", False) and row.get("recipe_family") == recipe_family and row.get("data_quality", {}).get("pass")]
    ranked = sorted(({"coil_id": row["coil_id"], "similarity": round(cosine_similarity(fingerprint, row["fingerprint"]), 3), "outcome": row.get("outcome"), "recorded_at": row.get("recorded_at")} for row in eligible), key=lambda item: item["similarity"], reverse=True)
    return ranked[:10]


def infer_risk(neighbors: list[dict[str, Any]], minimum_similarity: float = 0.85, minimum_evidence: int = 5) -> dict[str, Any]:
    usable = [n for n in neighbors if n["similarity"] >= minimum_similarity and n.get("outcome") in {"PASS", "DEFECT"}]
    if len(usable) < minimum_evidence:
        return {"status": "NOT_CALIBRATED", "message": "尚無足夠的高相似、已標註客戶歷史卷；不輸出失敗機率。", "evidence_count": len(usable)}
    raw_weights = [n["similarity"] ** 4 for n in usable]
    defect_rate = sum(weight * (n["outcome"] == "DEFECT") for weight, n in zip(raw_weights, usable)) / sum(raw_weights)
    return {"status": "ESTIMATED", "risk_score": round(defect_rate, 3), "evidence_count": len(usable), "message": "以相似且具最終檢驗標籤的歷史卷加權估計。"}


def physics_findings(features: dict[str, float], recipe: dict[str, Any]) -> list[dict[str, str]]:
    results = []
    soak_limit = recipe["acceptance_limits"]["soaking_stability_c"]["max"]
    if features["soaking_stability_c"] > soak_limit:
        results.append({"severity": "HIGH", "evidence": f"均熱段波動 {features['soaking_stability_c']}°C，規格上限 {soak_limit}°C", "suggestion": "檢查燃燒器輸出平衡、循環風機與溫度感測器漂移；需經現場 SOP 核准後才可調整。"})
    if abs(features["soaking_mean_error_c"]) > recipe["acceptance_limits"]["soaking_mean_error_c"]["max"]:
        results.append({"severity": "MEDIUM", "evidence": f"均熱均值偏差 {features['soaking_mean_error_c']}°C", "suggestion": "先核對配方 setpoint、鋼種與厚度對應，再由製程工程師判斷是否修正。"})
    if not results:
        results.append({"severity": "INFO", "evidence": "目前未發現本配方已定義的硬性違規。", "suggestion": "持續累積可追溯的最終品質結果，以校準未來風險模型。"})
    return results


def evaluate(csv_path: Path, coil_id: str, recipe: dict[str, Any], history: list[dict[str, Any]]) -> dict[str, Any]:
    times, temps, _ = load_curve_csv(csv_path)
    data_quality = score_data_quality(times, temps, recipe)
    source_hash = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    base = {"report_version": "guard-v2.0", "coil_id": coil_id, "recipe_family": recipe["recipe_family"], "source_file": csv_path.name, "source_sha256": source_hash, "evaluated_at": datetime.now(timezone.utc).isoformat(), "data_quality": data_quality, "is_demo_input": coil_id.upper().startswith("DEMO-")}
    if not data_quality["pass"]:
        return base | {"status": "DATA_REJECTED", "process_quality": None, "features": None, "fingerprint": None, "neighbors": [], "risk": {"status": "NOT_EVALUATED", "message": "資料品質未通過，未進行製程與風險推論。"}, "findings": []}
    features = extract_features(times, temps, recipe)
    process_quality = score_process(features, recipe)
    fingerprint = make_fingerprint(temps, features)
    neighbors = find_neighbors(fingerprint, history, coil_id, recipe["recipe_family"])
    return base | {"status": "PROCESS_PASS" if process_quality["pass"] else "PROCESS_ATTENTION", "process_quality": process_quality, "features": features, "fingerprint": fingerprint, "neighbors": neighbors, "risk": infer_risk(neighbors), "findings": physics_findings(features, recipe), "curve": [{"timestamp": value.isoformat(), "temp_c": temp} for value, temp in zip(times, temps)]}
