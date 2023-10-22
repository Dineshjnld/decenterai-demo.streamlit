import os.path
from functools import cache
from io import StringIO
from pathlib import Path

from typing import IO


@cache
def extract_css(css_file: str | IO | Path | StringIO) -> str:
    isFile = False

    if isinstance(css_file, str):
        isFile = os.path.exists(css_file)
        if not isFile:
            raise FileNotFoundError(css_file)
    cnt: str
    if isinstance(css_file, Path) or isFile:
        with open(css_file) as file:
            cnt = file.read()
    elif hasattr(css_file, "read"):  # IO
        cnt = css_file.read()
    else:
        raise ValueError("Invalid input type. Expected str, IO, or Path.")

    cnt = f"""
    <style>
    {cnt}
    </style>
    """.strip()

    return cnt
