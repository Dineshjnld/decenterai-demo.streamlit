import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def train_model(dataset):
    data = pd.read_csv(dataset)

    y = data.iloc[:, -1]
    X = data.iloc[:, :-1]

    print(X, y)

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression()
    # model.fit(X_train, y_train)

    model.fit(X, y)
    return model


if __name__ == "__main__":
    dataset = "income.csv"
    train_model(dataset)
