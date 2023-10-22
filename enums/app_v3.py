import logging
import os
import platform
import sys
import tempfile
import venv
from dataclasses import dataclass
from typing import Union

import streamlit as st
from dataclasses_json import dataclass_json, LetterCase
from streamlit.runtime.uploaded_file_manager import UploadedFile

from config import DEMO_DIR
from config.constants import (
    EXECUTION_ENVIRONMENT,
    JUPYTER_NOTEBOOK,
    MODE,
    PRODUCTION,
)
from utils.archive import archive_directory
import subprocess


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(slots=True)
class App:
    version: str = "v3"
    demo: bool = True
    _model_name: str = ""
    _prev_model_name: str = ""

    environment: EXECUTION_ENVIRONMENT = JUPYTER_NOTEBOOK
    training_script: str = None
    requirements_path: str = None
    _work_dir: str = None
    temp_dir: tempfile.TemporaryDirectory = None
    models_archive_dir = tempfile.TemporaryDirectory(
        prefix="decenter-ai-",
        suffix="-models-zip-dir",
    ).name

    python_repl: str = sys.executable
    venv_dir: str = None
    exit_success: bool = True

    _input_archive: UploadedFile | str = None

    _selected_demo: str = None

    def __post_init__(self):
        self.create_temporary_dir()  # create a temporary directory always

    @property
    def input_archive(self):
        return self._input_archive

    @input_archive.setter
    def input_archive(self, input_archive: UploadedFile | str):
        if not self._input_archive:
            logging.debug("input_archive: not found")
            self._input_archive = "samples/sample_v3"
            self.work_dir = "samples/sample_v3"
            self.demo = True
            return
        self.demo = False
        self._input_archive = input_archive
        logging.info(f"set input_archive: {input_archive}")

    @property
    def work_dir(self):
        return self._work_dir

    @work_dir.setter
    def work_dir(self, _work_dir: str):
        if not _work_dir:
            logging.warning("no work_dir found")
            return
        self._work_dir = _work_dir

    @property
    def model_name(self):
        return self._model_name

    @property
    def model_name_changed(self) -> bool:
        return self.model_name.strip() != self._prev_model_name.strip()

    @model_name.setter
    def model_name(self, model_name: str):
        if not model_name:
            st.toast("model name not changed")
            logging.debug("model_name: invalid")
            return
        self._prev_model_name = self._model_name
        self._model_name = model_name

        if self.model_name_changed:
            st.toast(
                f"model name updated from {self._prev_model_name} to {model_name}",
                icon="👌",
            )

    def create_venv(self, venv_dir=".venv"):
        venv_dir = os.path.join(self.work_dir, venv_dir)
        self.venv_dir = venv_dir

        venv.create(
            venv_dir,
            system_site_packages=True,
            with_pip=True,
            symlinks=False,  # TODO: disable in the future
        )

        logging.info("created venv dir")

        match platform.system():
            case "Windows":
                python_repl = os.path.join(venv_dir, "Scripts", "python.exe")
            case _:
                python_repl = os.path.join(venv_dir, "bin", "python3")

        self.python_repl = python_repl

        if MODE == PRODUCTION or True:
            logging.info(
                "installing jupyter",
            )  # FIXME: why streamlit app needs manual installation of jupyter debug..
            result = subprocess.run(
                [python_repl, "-m", "pip", "install", "jupyter"],
                cwd=self.work_dir,
                capture_output=True,
            )
            logging.info(result.stdout)
            logging.error(result.stderr)

    def export_working_dir(self, archive_name=None) -> Union[os.PathLike, str]:
        archive_name = archive_name or self.model_name

        zipfile_ = archive_directory(
            os.path.join(self.models_archive_dir, archive_name),
            self.work_dir,
        )
        # zipfile_ = archive_directory_in_memory(app.work_dir)
        return zipfile_

    def create_temporary_dir(self):
        self.temp_dir = tempfile.TemporaryDirectory(
            prefix="decenter-ai-",
            suffix=self.model_name,
        )
        self.work_dir = self.temp_dir.name

    @property
    def selected_demo(self):
        return self._selected_demo

    @selected_demo.setter
    def selected_demo(self, demo: str):
        self._selected_demo = demo
        if demo is None:
            return

        self.model_name = os.path.splitext(
            os.path.basename(self.selected_demo),
        )[0]

    def recycle_temp_dir(self):
        if isinstance(self.temp_dir, tempfile.TemporaryDirectory):
            logging.info(
                f"cleaning up the app:temp directory: {self.temp_dir.name}",
            )
            self.venv_dir = None
            self.temp_dir.cleanup()
        self.create_temporary_dir()

    @property
    def selected_demo_path(self):
        return os.path.join(DEMO_DIR, self.selected_demo)
