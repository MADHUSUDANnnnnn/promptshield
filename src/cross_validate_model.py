import pandas as pd
from pathlib import Path

from sklearn.model_selection import StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


def cross_validate_model():
    project_root = Path(__file__).resolve().parent.parent
    dataset_path = project_root / "data" / "promptshield_dataset.csv"

    df = pd.read_csv(dataset_path)

    X = df["prompt_text"]
    y = df["label"]

    skf = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []

    print("=" * 65)
    print("PROMPTSHIELD 5-FOLD CROSS-VALIDATION")
    print("=" * 65)

    fold_number = 1

    for train_index, test_index in skf.split(X, y):
        X_train = X.iloc[train_index]
        X_test = X.iloc[test_index]

        y_train = y.iloc[train_index]
        y_test = y.iloc[test_index]

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

        predictions = model.predict(X_test_vectorized)

        accuracy = accuracy_score(y_test, predictions)

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

        accuracies.append(accuracy)
        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1)

        print(f"\nFold {fold_number}")
        print(f"Accuracy:  {accuracy:.2%}")
        print(f"Precision: {precision:.2%}")
        print(f"Recall:    {recall:.2%}")
        print(f"F1 Score:  {f1:.2%}")

        fold_number += 1

    print("\n" + "=" * 65)
    print("AVERAGE CROSS-VALIDATION RESULTS")
    print("=" * 65)

    print(
        f"Average Accuracy:  "
        f"{sum(accuracies) / len(accuracies):.2%}"
    )

    print(
        f"Average Precision: "
        f"{sum(precisions) / len(precisions):.2%}"
    )

    print(
        f"Average Recall:    "
        f"{sum(recalls) / len(recalls):.2%}"
    )

    print(
        f"Average F1 Score:  "
        f"{sum(f1_scores) / len(f1_scores):.2%}"
    )


if __name__ == "__main__":
    cross_validate_model()