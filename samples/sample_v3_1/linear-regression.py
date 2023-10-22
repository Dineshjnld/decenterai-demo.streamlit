import time
from dataclasses import dataclass
from io import BytesIO
from typing import Union

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


@dataclass
class ModelTrainer:
    dataset: Union[BytesIO, "str"]
    pretrained_model: BytesIO = LinearRegression()

    train_test_split: int = 0.8

    X, y = None, None
    X_train, X_test, y_tain, y_test = [None] * 4
    trained_model = None

    def __post_init__(self):
        self.load_dataset()
        self.split_dataset(1 - self.train_test_split)

    def split_dataset(self, test_size=0.2, random_state=42, **kwargs):
        (
            self.X_train,
            self.X_test,
            self.y_train,
            self.y_test,
        ) = train_test_split(
            self.X,
            self.y,
            test_size=test_size,
            random_state=42,
            **kwargs,
        )  # use rand state for consistency

    def load_dataset(self):
        df = pd.read_csv(self.dataset)
        self.y = df["per_capita_income_in_usd"]
        self.X = df[["year"]]

    def train_model(self) -> "model":
        if self.X is None or self.y is None:
            raise ValueError("Dataset has not been loaded yet.")
        model = self.pretrained_model or LinearRegression()
        model.fit(self.X, self.y)
        self.trained_model = model
        return model

    def calculate_score(self, model=None, X=None, y=None) -> float:
        if model is None:
            model = self.trained_model

        if model is None:
            raise ValueError("Model missing")

        if X is None or y is None:
            X = self.X_test
            y = self.y_test

        if X is None or y is None:
            raise ValueError("Test data missing")

        _score = model.score(X, y)
        return _score


if __name__ == "__main__":
    # import joblib
    #
    # dataset = "canada_per_capita_income.csv"
    # # m1 = train_model(dataset)
    # # joblib.dump(m1, 'test-model.sav')
    # loaded_model = 'trained-model-2023-09-04 13_31_04.603032 0.010925s.sav'
    #
    # m2 = joblib.load(loaded_model)
    # train_model(dataset, m2)

    dataset = "canada_per_capita_income.csv"

    m1 = ModelTrainer(dataset)
    start_time = time.time()
    model = m1.train_model()
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.6f} seconds")

    score = m1.calculate_score()
    print(f"Model Score: {score * 100:0.3f}")

    joblib.dump(model, "model.joblib")
