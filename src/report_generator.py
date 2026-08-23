from pathlib import Path
from datetime import datetime
import json


def generate_report(prompt, result):
    project_root = Path(__file__).resolve().parent.parent

    reports_dir = project_root / "reports"
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now()

   

    txt_filename = (
        f"report_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
    )

    report_path = reports_dir / txt_filename

    report = []

    report.append("=" * 60)
    report.append("PROMPTSHIELD DETECTION REPORT")
    report.append("=" * 60)

    report.append(
        f"\nTimestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    report.append(f"\nPrompt:\n{prompt}")

    report.append(
        f"\nFinal Decision: "
        f"{'MALICIOUS' if result['is_malicious'] else 'BENIGN'}"
    )

    report.append(f"Risk Score: {result['risk_score']}")
    report.append(f"Risk Level: {result['risk_level']}")

    report.append(
        f"ML Probability: "
        f"{result['ml_probability']:.2%}"
    )

    report.append(
        f"Regex Rules Triggered: "
        f"{result['regex_rules_triggered']}"
    )

    report.append(
        "Detected Categories: "
        + (
            ", ".join(result["detected_categories"])
            if result["detected_categories"]
            else "None"
        )
    )

    report.append("=" * 60)

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("\n".join(report))

   

    json_filename = (
        f"report_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
    )

    json_path = reports_dir / json_filename

    json_report = {
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "prompt": prompt,
        "final_decision": (
            "MALICIOUS"
            if result["is_malicious"]
            else "BENIGN"
        ),
        "risk_score": result["risk_score"],
        "risk_level": result["risk_level"],
        "ml_probability": result["ml_probability"],
        "regex_rules_triggered": result["regex_rules_triggered"],
        "detected_categories": result["detected_categories"],
    }

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(
            json_report,
            file,
            indent=4
        )

    return report_path, json_path