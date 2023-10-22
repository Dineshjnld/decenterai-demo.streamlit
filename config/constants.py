import os
from typing import Final, TypeAlias, Literal

from dotenv import load_dotenv

load_dotenv()

PRODUCTION: Final[str] = "production"
DEVELOPMENT: Final[str] = "development"
TESTING: Final[str] = "testing"
MODE: Final[str] = os.getenv("mode", DEVELOPMENT)

#
# OPENAI_API_KEY: Final[str] = environ['OPENAI_API_KEY'].strip()
# OPENAI_ORGANIZATION_ID: Final[str] = environ.get(
#     'OPENAI_ORGANIZATION_ID', '',
# ).strip()
# OPENAI_EMBEDDINGS_LLM: Final[str] = os.getenv(
#     'OPENAI_EMBEDDINGS_LLM', 'text-embedding-ada-002',
# ).strip()
# OPENAI_CHAT_MODEL: Final[str] = os.getenv(
#     'OPENAI_CHAT_MODEL', 'gpt-3.5-turbo',
# ).strip()

PYTHON: Final = ".py"
JUPYTER_NOTEBOOK: Final = ".ipynb"
EXECUTION_ENVIRONMENT: TypeAlias = Literal[".py", ".ipynb"]

GITHUB_REPO: Final = (
    "https://github.com/DeCenter-AI/decenter-ai.streamlit.app/"
)
GITHUB_REPORT_BUG: Final = "https://github.com/DeCenter-AI/decenter-ai.streamlit.app/issues/new?assignees=&labels=kind%2Fbug&projects=&template=1-bug_report.yml"
GITHUB_ANY_ISSUE: Final = "https://github.com/DeCenter-AI/decenter-ai.streamlit.app/issues/new/choose"
GITHUB_DISCUSSION_QA: Final = "https://github.com/DeCenter-AI/decenter-ai.streamlit.app/discussions/new?category=q-a"
GITHUB_REQUEST_FEATURE: Final = "https://github.com/DeCenter-AI/decenter-ai.streamlit.app/issues/new?assignees=&labels=proposal%2C+enhancement&projects=&template=feature_request.md&title=feature-request%3A"

APP_ABOUT: Final = "https://bit.ly/decenterai"
