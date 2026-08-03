from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


def extract_disk_usage(disk_output: str) -> int:
    matches = re.findall(r"(\d+)%", disk_output)

    if not matches:
        raise ValueError("Keine Festplattenauslastung gefunden.")

    return int(matches[-1])


def evaluate_report(report: dict[str, Any]) -> dict[str, Any]:
    disk_usage_percent = extract_disk_usage(report["disk_output"])
    nginx_status = report.get("nginx_status", "unknown")

    findings: list[dict[str, str]] = []

    if disk_usage_percent >= 90:
        findings.append(
            {
                "severity": "critical",
                "component": "disk",
                "message": f"Festplattenauslastung kritisch: {disk_usage_percent} %",
            }
        )
    elif disk_usage_percent >= 75:
        findings.append(
            {
                "severity": "warning",
                "component": "disk",
                "message": f"Festplattenauslastung erhöht: {disk_usage_percent} %",
            }
        )

    if nginx_status != "running":
        findings.append(
            {
                "severity": "critical",
                "component": "nginx",
                "message": f"Nginx läuft nicht. Status: {nginx_status}",
            }
        )

    overall_status = "healthy"

    if any(item["severity"] == "critical" for item in findings):
        overall_status = "critical"
    elif findings:
        overall_status = "warning"

    return {
        "hostname": report.get("hostname", "unknown"),
        "status": overall_status,
        "disk_usage_percent": disk_usage_percent,
        "nginx_status": nginx_status,
        "findings": findings,
    }


def main() -> None:
    if len(sys.argv) != 2:
        print("Verwendung: python scripts/analyze_health_report.py <report.json>")
        raise SystemExit(1)

    report_path = Path(sys.argv[1])

    with report_path.open("r", encoding="utf-8") as file:
        report = json.load(file)

    result = evaluate_report(report)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
