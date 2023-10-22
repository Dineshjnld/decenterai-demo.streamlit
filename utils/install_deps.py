import concurrent.futures
import logging
import subprocess
import sys

import streamlit as st


def __install_deps(
    python_repl=sys.executable, requirements: list = None, cwd=None
):
    if not requirements:
        return

    print("install_deps", requirements)

    def install(package):
        subprocess.check_call(
            [python_repl, "-m", "pip", "install", package],
            stdout=st.info,
            stderr=st.error,
            universal_newlines=True,
        )

    # Use a ThreadPoolExecutor to install the packages in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(install, requirements)


@st.cache_resource
def install_dependencies(
    python_repl=sys.executable,
    requirements_path=None,
    requirements=None,
    cwd=None,
):
    if requirements:
        logging.info("install_dependencies:")
        __install_deps(python_repl, requirements, cwd)

    if not requirements_path:
        logging.warning("install_dependencies:requirements_path not found")
        return

    print("installing dependencies:  for ", python_repl)
    command = [python_repl, "-m", "pip", "install", "-r", requirements_path]
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        encoding="UTF-8",
    )

    logging.info(result.stdout)
    logging.error(result.stderr)

    st.toast(result.stdout)
    st.toast(result.stderr)
    return result


@st.cache_resource
def install_dependencies_v0(requirements_txt):
    if not requirements_txt:
        return
    requirements = requirements_txt

    def install(package):
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package],
        )

    # Use a ThreadPoolExecutor to install the packages in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(install, requirements)

    # for package in requirements:
    #     subprocess.check_call([sys.executable, "-m", "pip", "install", package])
