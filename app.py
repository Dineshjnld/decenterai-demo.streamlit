import logging
import shutil
import subprocess
import sys
import zipfile
from typing import List

import streamlit as st

from config.constants import *
from config.log import setup_log
from enums.app_v3 import App
from utils.exec_commands import get_notebook_cmd
from utils.helper_find import (
    find_requirements_txt_files,
    find_driver_scripts,
    find_demos,
)
from utils.install_deps import install_dependencies
from views.head import head_v3

setup_log()

load_dotenv()

head_v3()

option = st.selectbox(
    "App Version",
    ("v3", "v2", "v1"),
    help="versioning documentation with feature lists coming up soon",
)

app: App = st.session_state.get("app")

if not app:
    app = App()
    logging.info("creating new app instance")
    st.session_state.app = app


if option != app.version:  # don't redirect if in the same page
    st.markdown(
        f'<meta http-equiv="refresh" content="0;URL=/{option}">',
        unsafe_allow_html=True,
    )

app.selected_demo = st.selectbox(
    "Demo",
    find_demos(),
    help="enabled when no input archive is uploaded",
    disabled=not app.demo,
    key="selected_demo",
)

input_archive = st.file_uploader(
    "Upload Training Workspace Archive with Datasets",
    type=["zip"],
    key="input_archive",
    help="Include trainscript[.py,ipynb] and datasets",
)

demo = input_archive is None

if demo != app.demo:
    app.demo = demo
    logging.info(f"demo mode set {app.demo}->{demo}")
    st.experimental_rerun()

if not app.demo and input_archive:
    model_name = os.path.splitext(os.path.basename(input_archive.name))[0]
    app.model_name = model_name

if not app.demo:
    model_name = st.text_input(
        "Model Name",
        max_chars=50,
        placeholder="decenter-model",
        key="model_name",
        value=app.model_name,
        disabled=app.demo,
    )
    if model_name and app.model_name != model_name:
        app.model_name = model_name

if app.model_name not in app.work_dir:
    logging.info("creating new app.work_dir")
    app.recycle_temp_dir()

if app.demo:
    if not app.selected_demo:
        st.error("demo: not found")
        logging.critical("demo: not found")
        st.stop()

    with zipfile.ZipFile(app.selected_demo_path, "r") as zip_ref:
        zip_ref.extractall(app.work_dir)

    app.python_repl = sys.executable
else:
    with zipfile.ZipFile(input_archive, "r") as zip_ref:
        zip_ref.extractall(app.work_dir)

    extracted_files = os.listdir(app.work_dir)
    logging.info(f"extracted: {extracted_files}")
    logging.info(f"work_dir: {app.work_dir}")

    app.create_venv()

app.training_script = st.selectbox(
    "Training Script:",
    find_driver_scripts(app.work_dir),
)

if not app.training_script:
    logging.critical("starter_script:not found")
    st.error("starter_script:not found; app exiting")
    st.stop()

execution_environment: str = os.path.splitext(app.training_script)[1]
training_cmd: List[str]

match execution_environment:
    case ".py":
        app.environment = PYTHON
        requirements = st.selectbox(
            "Select dependencies to install",
            find_requirements_txt_files(
                app.work_dir,
            ),
        )

        if requirements:
            with st.spinner("Installing dependencies in progress"):
                app.requirements_path = os.path.join(
                    app.work_dir,
                    requirements,
                )
                install_dependencies(
                    app.python_repl,
                    app.requirements_path,
                    cwd=app.work_dir,
                )
        training_cmd = [app.python_repl, app.training_script]

    case ".ipynb":
        app.environment = JUPYTER_NOTEBOOK

        training_cmd = get_notebook_cmd(
            app.training_script,
            app.python_repl,
        )

    case _:
        st.error("invalid trainer script-Raise issue")
        logging.critical(f"invalid trainer script- {app.training_script}")
        st.stop()

if not training_cmd:
    st.error("invalid training_cmd-Raise Issue")
    st.stop()

if st.button("Train", key="train"):
    logging.info(f"starter_script - {app.training_script}")
    st.snow()

    with st.spinner("Training in progress"):
        result = subprocess.run(
            training_cmd,
            cwd=app.work_dir,
            capture_output=True,
            encoding="UTF-8",
        )

        logging.info(result.stdout)
        logging.error(result.stderr)

        with open(os.path.join(app.work_dir, "stdout"), "w") as stdout, open(
            os.path.join(app.work_dir, "stderr"),
            "w",
        ) as stderr:
            stdout.write(result.stdout)
            stderr.write(result.stderr)

        if result.stdout:
            st.info(result.stdout)

        if result.stderr:
            st.warning(result.stderr)

        if app.environment is JUPYTER_NOTEBOOK:
            out = f"{app.training_script}.html"
            if os.path.exists(
                os.path.join(app.work_dir, f"{app.training_script}.html"),
            ):
                st.info(f"notebook: output generated at {out}")
                logging.info(f"notebook: output generated at {out}")
            else:
                app.exit_success = False
                st.error("notebook: execution failed")
                logging.error("notebook: execution failed")

    if not app.exit_success:
        logging.critical(f"env:{app.environment}:failed")
        st.error("app execution failed")
        st.stop()

    if app.venv_dir:
        shutil.rmtree(app.venv_dir)

    model_output = app.export_working_dir()

    st.toast("Model Trained successfully!", icon="🧤")

    st.success("Model Training Request completed successfully!", icon="✅")

    st.balloons()

    with open(model_output, "rb") as f1:
        st.download_button(
            label="Download Model",
            data=f1,
            file_name=f"decenter-model-{app.model_name}.zip",
            key="download_model",
        )
        app.recycle_temp_dir()
