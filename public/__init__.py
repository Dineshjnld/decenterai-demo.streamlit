from config.constants import GITHUB_REQUEST_FEATURE, GITHUB_REPORT_BUG
from utils.inputs.css import extract_css
from utils.inputs.html import extract_html

public_dir = "static/"

index_css = extract_css(f"static/index.css")

# index_css = """
# <link href="./static/index.css" rel="stylesheet">
# """

logo = "static/logo.png"

report_request_buttons_html = extract_html(
    f"public/report-request-feature-buttons.html",
).format(
    REPORT_BUG_URL=GITHUB_REPORT_BUG,
    REQUEST_A_FEATURE=GITHUB_REQUEST_FEATURE,
)

button_styles_css = extract_css("public/buttons.css")
