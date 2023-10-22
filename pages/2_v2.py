import importlib.util

import joblib
import streamlit as st
from sklearn.linear_model import LinearRegression

from enums.model_trainer import ModelTrainer
from models.model import c, getModelTrainer
from utils.format_display_code import format_python_code
from utils.install_deps import install_dependencies_v0
from views.head import head
from views.train import train

progress = 10


def update_progress(number: int):
    progress_bar.progress(number)


st.sidebar.header("v2")

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

head()

update_progress(20)

# @st.cache_data
# def get_python_code(filename: str, label: str):
#     return

# model_name = st.text_input('Enter a model name: ', value=f'model')
model_name = st.text("model: sklearn.linear_model.Linear Regression")

m1: ModelTrainer = getModelTrainer(model_name)

update_progress(30)


# python_code = st.file_uploader('Upload Training Python Script', type=['py'])

with open("samples/sample_v2/linear-regression.py") as f1:
    training_code = f1.read()
    # python_code = base64.b64encode(file_content)

# with st.echo():
#     st.write('This code will be printed')

if training_code and st.checkbox("Show Code"):
    # display_code = format_python_code(python_code.getvalue().decode())
    display_code = format_python_code(training_code)
    st.code(display_code, language="python")

dataset = st.file_uploader("Upload Dataset", type=["csv"])
# requirements_txt = st.file_uploader('Upload requirements.txt', type=['txt'])
requirements_txt = ""

if not dataset:
    st.warning("Dataset not found: uploading a predefined dataset")
    dataset = "samples/sample_v2/canada_per_capita_income.csv"

train_split_ratio = st.number_input(
    "Train Split Ratio (%)",
    min_value=0,
    max_value=100,
    value=80,
)

update_progress(50)

# train_split_ratio = 100

if requirements_txt:

    @st.experimental_memo
    def retrieve_requirements():  # @todo TODO: use in other pages https://discuss.streamlit.io/t/caching-uploaded-file-while-using-multipage/26287/3
        uploaded_file = requirements_txt
        return uploaded_file

    # requirements_txt.getvalue().decode().split('\n')
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

if training_code and dataset:
    module_name = "__temp_module__"
    spec = importlib.util.spec_from_loader(module_name, loader=None)
    module = importlib.util.module_from_spec(spec)
    # spec.loader.load_module() #FIXME: install and inject deps to the module only
    # Compile and execute the code within the module
    exec(training_code, module.__dict__)

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

    if not pretrained_model:
        st.warning("Pretrained model not found: uploading base model")
        loaded_model = LinearRegression()

    if pretrained_model:
        if st.button("Score: Pretrained Model"):
            score_placeholder = m1.calculate_score(loaded_model)  # m1.X, m1.y
            display_score = round(score_placeholder * 100, 2)

            html_string = f"<div class=w3-light-grey><div class=w3-pro id=pretrained  style=width:{display_score}%>{display_score}%</div></div><br>"
            st.write(f"Pretrained-Model Score")

            st.markdown(html_string, unsafe_allow_html=True)

            # st.write(f"Pretrained-Model Score: {score_placeholder * 100:0.3f}%")
update_progress(100)

if st.button("Train"):
    if not training_code:
        st.error("Please upload Python code to train the model.")

    if not dataset:
        st.warning("Please upload the dataset to train or test the model")

    if training_code and dataset:
        st.snow()
        train(model_name)
        st.balloons()
