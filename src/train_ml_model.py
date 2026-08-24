import joblib
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix


def train_model():
    project_root = Path(__file__).resolve().parent.parent
    dataset_path = project_root / "data" / "promptshield_dataset.csv"

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

    print("=" * 60)
    print("PROMPTSHIELD ML MODEL TRAINING")
    print("=" * 60)

    print(f"\nTotal prompts: {len(df)}")
    print(f"Training prompts: {len(X_train)}")
    print(f"Testing prompts: {len(X_test)}")

    print("\nCLASSIFICATION REPORT")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0,
        )
    )

    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, predictions))

    print("=" * 60)

    models_directory = project_root / "models"
    models_directory.mkdir(exist_ok=True)

    model_path = models_directory / "promptshield_model.joblib"
    vectorizer_path = models_directory / "tfidf_vectorizer.joblib"

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

    print("\nMODEL FILES SAVED")
    print(f"Model: {model_path}")
    print(f"Vectorizer: {vectorizer_path}")


if __name__ == "__main__":
    train_model()