import pandas as pd
from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from hybrid_detector import detect_prompt


def evaluate_hybrid_detector():
    project_root = Path(__file__).resolve().parent.parent
    dataset_path = project_root / "data" / "promptshield_dataset.csv"

    df = pd.read_csv(dataset_path)

    actual_labels = []
    predicted_labels = []

    for _, row in df.iterrows():
        actual_label = row["label"]

        result = detect_prompt(row["prompt_text"])

        predicted_label = (
            1 if result["is_malicious"] else 0
        )

        actual_labels.append(actual_label)
        predicted_labels.append(predicted_label)

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

    true_negative = matrix[0][0]
    false_positive = matrix[0][1]
    false_negative = matrix[1][0]
    true_positive = matrix[1][1]

    print("=" * 60)
    print("PROMPTSHIELD HYBRID DETECTOR EVALUATION")
    print("=" * 60)

    print(f"\nTotal prompts: {len(df)}")

    print("\nPERFORMANCE METRICS")

    print(f"Accuracy:  {accuracy:.2%}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall:    {recall:.2%}")
    print(f"F1 Score:  {f1:.2%}")

    print("\nCONFUSION MATRIX")

    print(f"True Negatives:  {true_negative}")
    print(f"False Positives: {false_positive}")
    print(f"False Negatives: {false_negative}")
    print(f"True Positives:  {true_positive}")

    print("=" * 60)


if __name__ == "__main__":
    evaluate_hybrid_detector()