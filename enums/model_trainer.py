from abc import ABC, abstractmethod
from dataclasses import dataclass
from io import BytesIO
from typing import TypeVar, Union

Model = TypeVar('Model')


@dataclass
class ModelTrainer(ABC):
    dataset: Union[BytesIO, 'str']
    pretrained_model: BytesIO

    train_test_split: int = 0.8

    X, y = None, None
    X_train, X_test, y_tain, y_test = [None] * 4
    trained_model = None

    @abstractmethod
    def __post_init__(self):
        pass

    @abstractmethod
    def split_dataset(self, test_size=0.2, random_state=42, **kwargs):
        pass

    @abstractmethod
    def load_dataset(self):
        pass

    @abstractmethod
    def train_model(self) -> Model:
        pass

    @abstractmethod
    def calculate_score(self, model=None, X=None, y=None) -> float:
        pass
