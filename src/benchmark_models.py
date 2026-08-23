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
    confusion_matrix,
)

from regex_detector import detect_regex


def calculate_metrics(actual, predicted):
    return {
        "accuracy": accuracy_score(actual, predicted),
        "precision": precision_score(
            actual,
            predicted,
            zero_division=0,
        ),
        "recall": recall_score(
            actual,
            predicted,
            zero_division=0,
        ),
        "f1": f1_score(
            actual,
            predicted,
            zero_division=0,
        ),
        "matrix": confusion_matrix(actual, predicted),
    }


def print_results(detector_name, results):
    print("\n" + "=" * 60)
    print(detector_name)
    print("=" * 60)

    print(f"Accuracy:  {results['accuracy']:.2%}")
    print(f"Precision: {results['precision']:.2%}")
    print(f"Recall:    {results['recall']:.2%}")
    print(f"F1 Score:  {results['f1']:.2%}")

    print("\nConfusion Matrix:")
    print(results["matrix"])


def benchmark_models():
    project_root = Path(__file__).resolve().parent.parent

    dataset_path = (
        project_root
        / "data"
        / "promptshield_dataset.csv"
    )

    df = pd.read_csv(dataset_path)

    X = df["prompt_text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print("=" * 60)
    print("PROMPTSHIELD FAIR BENCHMARK")
    print("=" * 60)

    print(f"\nTraining prompts: {len(X_train)}")
    print(f"Unseen testing prompts: {len(X_test)}")

    # -------------------------
    # REGEX DETECTOR
    # -------------------------

    regex_predictions = []

    for prompt in X_test:
        result = detect_regex(prompt)

        prediction = (
            1 if result["is_malicious"] else 0
        )

        regex_predictions.append(prediction)

    regex_results = calculate_metrics(
        y_test,
        regex_predictions,
    )

    # -------------------------
    # ML DETECTOR
    # -------------------------

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

    ml_predictions = model.predict(
        X_test_vectorized
    )

    ml_results = calculate_metrics(
        y_test,
        ml_predictions,
    )

    # -------------------------
    # HYBRID DETECTOR
    # -------------------------

    hybrid_predictions = []

    for regex_prediction, ml_prediction in zip(
        regex_predictions,
        ml_predictions,
    ):
        hybrid_prediction = int(
            regex_prediction == 1
            or ml_prediction == 1
        )

        hybrid_predictions.append(hybrid_prediction)

    hybrid_results = calculate_metrics(
        y_test,
        hybrid_predictions,
    )

    # -------------------------
    # PRINT RESULTS
    # -------------------------

    print_results(
        "REGEX DETECTOR RESULTS",
        regex_results,
    )

    print_results(
        "ML DETECTOR RESULTS",
        ml_results,
    )

    print_results(
        "HYBRID DETECTOR RESULTS",
        hybrid_results,
    )


if __name__ == "__main__":
    benchmark_models()