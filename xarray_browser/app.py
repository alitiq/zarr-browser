""" index / central page handling for visualisation of district heating forecasts and analysis """

from dash.dependencies import Input, Output, State
import os
from xarray_browser.templates.base import base_layout
from xarray_browser.server import app, server

from xarray_browser.callbacks.file_listing import (  # noqa:F401
    toggle_directory,
    generate_directory_listing,
    display_file_system_page
)
from xarray_browser.callbacks.xarray_html import (  # noqa:F401
    display_xarray_html
)

app.layout = base_layout()



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 443))
    server.run(
        host="0.0.0.0",
        port=port,
        threaded=False,
        processes=4,
        # ssl_context=(
        #     os.environ["SSL_CERT_PATH"],
        #     os.environ["SSL_KEY_PATH"],
        # ),  # noqa: S104
    )
