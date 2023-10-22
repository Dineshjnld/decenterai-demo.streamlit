import io
import time

import joblib
import streamlit as st
from colorama import Fore

from models.model import getModelTrainer


def train(model_name: str):  # if python_code and dataset:
    m1 = getModelTrainer(model_name)

    status_placeholder = st.empty()
    score_placeholder = st.empty()
    bar = st.progress(20)

    start_time = time.time()
    model = m1.train_model()
    end_time = time.time()

    elapsed_time = end_time - start_time

    status_placeholder.text(f"Training complete, took {elapsed_time:.6f}s")

    bar.progress(80)

    print(f"{Fore.CYAN} Elapsed time: {elapsed_time:.6f} sec {Fore.RESET}")

    fName = f"trained-{model_name}-{elapsed_time:.6f}s.sav"

    model_bytes = io.BytesIO()
    joblib.dump(m1.trained_model, model_bytes)
    model_bytes.seek(0)

    # st.write("Trained a new model")

    score = m1.calculate_score()

    bar.progress(100)

    status_placeholder.text(f"Training Duration: {elapsed_time:.6f}s")
    # score_placeholder.text(f"Trained Model Score: {score * 100:0.3f}%")

    html_string = "<div class=w3-light-grey><div class=w3-pro id=trained  style=width:{percentage_complete}%>{percentage_complete}%</div></div><br>".format(
        percentage_complete=round(score * 100, 2),
    )
    st.write(f"Trained Model Score")
    st.markdown(html_string, unsafe_allow_html=True)

    # if st.button('Score: Trained Model'):
    #     score = m1.calculate_score(m1.trained_model, m1.X, m1.y)
    #     st.write(f"Trained Model Score: {score * 100:0.3f}")

    st.download_button(
        label="Download trained model",
        data=model_bytes,
        file_name=fName,
    )
