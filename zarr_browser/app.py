""" plotly dash app for  """

import os
from zarr_browser.templates.base import base_layout
from zarr_browser.server import app, server

from zarr_browser.callbacks.file_system import (  # noqa:F401
    toggle_directory,
    generate_directory_listing,
    display_file_system_page,
)
from zarr_browser.callbacks.zarr_visualisation import display_xarray_html  # noqa:F401

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
