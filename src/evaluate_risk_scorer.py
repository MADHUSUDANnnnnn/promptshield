import pandas as pd
from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from risk_scorer import calculate_risk


def evaluate_risk_scorer():
    project_root = Path(__file__).resolve().parent.parent

    dataset_path = (
        project_root
        / "data"
        / "promptshield_dataset.csv"
    )

    df = pd.read_csv(dataset_path)

    actual_labels = []
    predicted_labels = []
    risk_scores = []

    for _, row in df.iterrows():
        result = calculate_risk(row["prompt_text"])

        actual_labels.append(row["label"])

        predicted_labels.append(
            1 if result["is_malicious"] else 0
        )

        risk_scores.append(result["risk_score"])

    accuracy = accuracy_score(
        actual_labels,
        predicted_labels,
    )

    precision = precision_score(
        actual_labels,
        predicted_labels,
        zero_division=0,
    )

    recall = recall_score(
        actual_labels,
        predicted_labels,
        zero_division=0,
    )

    f1 = f1_score(
        actual_labels,
        predicted_labels,
        zero_division=0,
    )

    matrix = confusion_matrix(
        actual_labels,
        predicted_labels,
    )

    print("=" * 60)
    print("PROMPTSHIELD RISK SCORER EVALUATION")
    print("=" * 60)

    print(f"\nTotal prompts: {len(df)}")

    print("\nPERFORMANCE METRICS")

    print(f"Accuracy:  {accuracy:.2%}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall:    {recall:.2%}")
    print(f"F1 Score:  {f1:.2%}")

    print("\nCONFUSION MATRIX")

    print(matrix)

    print("\nRISK SCORE INFORMATION")

    print(
        f"Minimum score: "
        f"{min(risk_scores):.2f}"
    )

    print(
        f"Maximum score: "
        f"{max(risk_scores):.2f}"
    )

    print(
        f"Average score: "
        f"{sum(risk_scores) / len(risk_scores):.2f}"
    )

    print("=" * 60)


if __name__ == "__main__":
    evaluate_risk_scorer()