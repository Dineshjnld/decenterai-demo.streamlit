import cachetools
import streamlit as st

from enums.model_trainer import ModelTrainer

c = cachetools.Cache(maxsize=100)

if "models" not in st.session_state:
    print("models not found")
    st.session_state.models = c
else:
    print("models found")
    c = st.session_state.models


def getModelTrainer(model_name: str) -> ModelTrainer:
    return c.get(model_name)
