import app as streamlit_app

from enums.app_v3 import App
from utils.helper_find import find_demos


def test_app():
    assert isinstance(streamlit_app.app, App)

    app: App = streamlit_app.app  # st.session_state.get("app")

    assert isinstance(app.model_name, str) is True
    assert app.model_name == find_demos()[0].strip(".zip")
    assert app.demo is True
