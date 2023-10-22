import importlib.util

import joblib
import streamlit as st

from enums.model_trainer import ModelTrainer
from models.model import c, getModelTrainer
from utils.format_display_code import format_python_code
from utils.install_deps import install_dependencies_v0
from views.head import head
from views.train import train

head()

# @st.cache_data
# def get_python_code(filename: str, label: str):
#     return

model_name = st.text_input("Enter a model name: ", value=f"model")

m1: ModelTrainer = getModelTrainer(model_name)

# with open('samples/linear-regression.py', 'r') as f1:
#     python_code = f1.read()
# dataset: str = dataset or 'samples/canada_per_capita_income.csv'

python_code = st.file_uploader("Upload Python Code", type=["py"])

# with st.echo():
#     st.write('This code will be printed')
if python_code and st.checkbox("Show Code"):
    display_code = format_python_code(python_code.getvalue().decode())
    st.code(display_code, language="python")

dataset = st.file_uploader("Upload Dataset", type=["csv"])
requirements_txt = st.file_uploader("Upload requirements.txt", type=["txt"])


train_split_ratio = st.number_input(
    "Train Split Ratio (%)",
    min_value=0,
    max_value=100,
    value=80,
)

if requirements_txt:

    @st.experimental_memo
    def retrieve_requirements():  # @todo TODO: use in other pages https://discuss.streamlit.io/t/caching-uploaded-file-while-using-multipage/26287/3
        uploaded_file = requirements_txt
        return uploaded_file

    install_dependencies_v0(requirements_txt)

    # FIXME: add icon william
    # st.download_button(
    # label="download", #FIXME: add icon instead
    # data=requirements_txt,
    # file_name="requirements.txt",
    # )
    # st.markdown("<a href='data:application/octet-stream;base64," + base64.b64encode(requirements_txt.read()).decode() +
    #             "' download='requirements.txt'><img src='data:image/png;base64,iVBORw0KG...'></a>",
    #             unsafe_allow_html=True)

loaded_model = None

if python_code and dataset:
    module_name = "__temp_module__"
    spec = importlib.util.spec_from_loader(module_name, loader=None)
    module = importlib.util.module_from_spec(spec)
    # spec.loader.load_module() #FIXME: install and inject deps to the module only
    # Compile and execute the code within the module
    exec(python_code.getvalue(), module.__dict__)

    m1: ModelTrainer = module.__dict__["ModelTrainer"](
        dataset,
        loaded_model,
        train_test_split=train_split_ratio / 100,
    )

    c[model_name] = m1

    pretrained_model = st.file_uploader(
        "Upload Pretrained Model",
        type=["sav"],
    )

    if pretrained_model:
        loaded_model = joblib.load(pretrained_model)
        st.write("Loaded pretrained model.")

        if st.button("Score: Pretrained Model"):
            score_placeholder = m1.calculate_score(loaded_model)  # m1.X, m1.y
            display_score = round(score_placeholder * 100, 2)

            html_string = f"<div class=w3-light-grey><div class=w3-pro id=pretrained  style=width:{display_score}%>{display_score}%</div></div><br>"
            st.write(f"Pretrained-Model Score")

            st.markdown(html_string, unsafe_allow_html=True)

            # st.write(f"Pretrained-Model Score: {score_placeholder * 100:0.3f}%")

if st.button("Train"):
    if not python_code:
        st.error("Please upload Python code to train the model.")

    if not dataset:
        st.warning("Please upload the dataset to train or test the model")

    if python_code and dataset:
        st.snow()
        train(model_name)
        st.balloons()
