import pandas as pd
from pathlib import Path

from regex_detector import detect_regex


def analyze_errors():
    project_root = Path(__file__).resolve().parent.parent
    dataset_path = (
        project_root / "data" / "promptshield_dataset.csv"
    )

    df = pd.read_csv(dataset_path)

    false_positives = []
    false_negatives = []

    for _, row in df.iterrows():
        result = detect_regex(row["prompt_text"])

        predicted_label = (
            1 if result["is_malicious"] else 0
        )

        actual_label = row["label"]

        if actual_label == 0 and predicted_label == 1:
            false_positives.append(row)

        elif actual_label == 1 and predicted_label == 0:
            false_negatives.append(row)

    print("=" * 60)
    print("PROMPTSHIELD REGEX ERROR ANALYSIS")
    print("=" * 60)

    print(f"\nFalse positives: {len(false_positives)}")
    print(f"False negatives: {len(false_negatives)}")

    print("\nMISSED ATTACKS BY CATEGORY")

    if false_negatives:
        false_negative_df = pd.DataFrame(false_negatives)

        print(
            false_negative_df[
                "attack_category"
            ].value_counts()
        )

        print("\nSAMPLE MISSED ATTACKS")

        for _, row in false_negative_df.head(10).iterrows():
            print("\n" + "-" * 60)
            print(f"ID: {row['prompt_id']}")
            print(f"Category: {row['attack_category']}")
            print(f"Prompt: {row['prompt_text']}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    analyze_errors()