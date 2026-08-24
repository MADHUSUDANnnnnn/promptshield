import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

from regex_detector import detect_regex


def tune_threshold():
    project_root = Path(__file__).resolve().parent.parent
    dataset_path = project_root / "data" / "promptshield_dataset.csv"

    df = pd.read_csv(dataset_path)

    X_train, X_test, y_train, y_test = train_test_split(
        df["prompt_text"],
        df["label"],
        test_size=0.20,
        random_state=42,
        stratify=df["label"],
    )

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        max_features=5000,
    )

    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    model = LogisticRegression(
        max_iter=1000,
        random_state=42,
        class_weight="balanced",
    )

    model.fit(X_train_vectorized, y_train)

    ml_probabilities = model.predict_proba(
        X_test_vectorized
    )[:, 1]

    risk_scores = []

    for prompt, ml_probability in zip(
        X_test,
        ml_probabilities,
    ):
        regex_result = detect_regex(prompt)

        triggered_rules = len(
            regex_result["triggered_rules"]
        )

        ml_score = ml_probability * 70
        regex_score = min(triggered_rules * 15, 30)

        final_score = min(
            ml_score + regex_score,
            100,
        )

        risk_scores.append(final_score)

    thresholds = [30, 35, 40, 45, 50, 55, 60, 65, 70]

    print("=" * 70)
    print("PROMPTSHIELD RISK THRESHOLD TUNING")
    print("=" * 70)

    print(
        f"\n{'Threshold':<12}"
        f"{'Accuracy':<12}"
        f"{'Precision':<12}"
        f"{'Recall':<12}"
        f"{'F1 Score':<12}"
    )

    print("-" * 70)

    for threshold in thresholds:
        predictions = [
            1 if score >= threshold else 0
            for score in risk_scores
        ]

        accuracy = accuracy_score(
            y_test,
            predictions,
        )

        precision = precision_score(
            y_test,
            predictions,
            zero_division=0,
        )

        recall = recall_score(
            y_test,
            predictions,
            zero_division=0,
        )

        f1 = f1_score(
            y_test,
            predictions,
            zero_division=0,
        )

        print(
            f"{threshold:<12}"
            f"{accuracy:<12.2%}"
            f"{precision:<12.2%}"
            f"{recall:<12.2%}"
            f"{f1:<12.2%}"
        )

    print("=" * 70)


if __name__ == "__main__":
    tune_threshold()