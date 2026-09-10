"""Command line entrypoint for the Curve OS Guard commercial prototype."""
from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path

from curve_os_core import ROOT, evaluate, read_json, write_json


CONFIG = ROOT / "config" / "recipe_catalog.json"
HISTORY = ROOT / "data" / "history" / "coil_records.json"
RUNTIME = ROOT / "data" / "runtime"
DEMO_INPUT = ROOT / "data" / "incoming" / "DEMO-B20260824-001.csv"


def create_demo_curve(path: Path) -> None:
    """Create a clearly labelled synthetic input, never a customer result."""
    start = datetime(2026, 8, 24, 0, 0, tzinfo=timezone.utc)
    rows = []
    for index in range(90):
        if index < 30:
            temp = 520 + 7.3 * index + math.sin(index * 0.7) * 1.4
            target = 650
        elif index < 60:
            temp = 750 + math.sin(index * 0.9) * 4.0 + math.sin(index * 0.2) * 2.0
            target = 750
        else:
            temp = 750 - 5.1 * (index - 60) + math.sin(index * 0.5) * 1.2
            target = 650
        rows.append({"timestamp": (start + timedelta(minutes=index)).isoformat(), "temp_c": round(temp, 2), "setpoint_c": target})
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["timestamp", "temp_c", "setpoint_c"])
        writer.writeheader()
        writer.writerows(rows)


def ensure_demo_assets() -> None:
    if not DEMO_INPUT.exists():
        create_demo_curve(DEMO_INPUT)
    if not HISTORY.exists():
        write_json(HISTORY, [])


def run_evaluation(input_path: Path, coil_id: str) -> dict:
    ensure_demo_assets()
    report = evaluate(input_path, coil_id, read_json(CONFIG), read_json(HISTORY))
    RUNTIME.mkdir(parents=True, exist_ok=True)
    write_json(RUNTIME / "latest_report.json", report)
    with (RUNTIME / "audit_log.jsonl").open("a", encoding="utf-8") as log:
        log.write(json.dumps({key: report[key] for key in ["evaluated_at", "coil_id", "status", "source_sha256", "report_version"]}, ensure_ascii=False) + "\n")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Curve OS Guard 離線品質與製程判讀")
    parser.add_argument("--input", type=Path, default=DEMO_INPUT, help="CSV：timestamp,temp_c[,setpoint_c]")
    parser.add_argument("--coil-id", default="DEMO-B20260824-001")
    parser.add_argument("--init-demo", action="store_true", help="建立明確標記的示範輸入檔")
    args = parser.parse_args()
    ensure_demo_assets()
    if args.init_demo:
        print(f"已建立示範資料：{DEMO_INPUT}")
        return
    report = run_evaluation(args.input, args.coil_id)
    print(f"[{report['status']}] Coil: {report['coil_id']}")
    print(f"資料品質: {report['data_quality']['score']}")
    if report["process_quality"]:
        print(f"製程合規: {report['process_quality']['score']}")
    print(f"風險推論: {report['risk']['status']}")
    print(f"報告：{RUNTIME / 'latest_report.json'}")


if __name__ == "__main__":
    main()
