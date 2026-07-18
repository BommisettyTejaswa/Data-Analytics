import pandas as pd

from utils.preprocessing import clean_dataset, split_dataset


def test_clean_dataset_and_split_ratio():
    df = pd.DataFrame(
        {
            "Age": [25, 30, None, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 110, 120, 130, 140, 150],
            "Sex": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            "ChestPainType": ["TA", "ATA", None, "NAP", "ASYM", "TA", "ATA", "NAP", "ASYM", "TA", "ATA", "NAP", "ASYM", "TA", "ATA", "NAP", "ASYM", "TA", "ATA", "NAP"],
            "HeartDisease": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        }
    )

    cleaned = clean_dataset(df)

    assert cleaned.isna().sum().sum() == 0
    assert len(cleaned) == 20

    X_train, X_test, y_train, y_test = split_dataset(cleaned, test_size=0.2)

    assert len(X_train) == 16
    assert len(X_test) == 4
    assert len(y_train) == 16
    assert len(y_test) == 4
