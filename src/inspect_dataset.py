import pandas as pd
from pathlib import Path


def inspect_dataset():
    project_root = Path(__file__).resolve().parent.parent
    dataset_path = project_root / "data" / "promptshield_dataset.csv"

    print("=" * 50)
    print("PROMPTSHIELD DATASET INSPECTION")
    print("=" * 50)

    df = pd.read_csv(dataset_path)

    print("\nDataset loaded successfully!")

    print("\nDataset shape:")
    print(df.shape)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nDataset information:")
    df.info()

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())


if __name__ == "__main__":
    inspect_dataset()