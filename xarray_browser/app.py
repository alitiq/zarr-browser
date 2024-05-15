""" index / central page handling for visualisation of district heating forecasts and analysis """

from dash.dependencies import Input, Output, State
import os
from xarray_browser.templates.base import base_layout
from xarray_browser.server import app, server

from xarray_browser.callbacks.file_listing import (  # noqa:F401
    toggle_directory,
    generate_directory_listing,
)

app.layout = base_layout()


@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")],
             [State('open-dirs', 'data')])
def display_page(pathname, open_dirs):
    """main window content handler"""
    if pathname == '/' or pathname == '/browse':
        pathname = os.environ['ROOT_DIR']
    return generate_directory_listing(os.environ['ROOT_DIR'], open_dirs)



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
