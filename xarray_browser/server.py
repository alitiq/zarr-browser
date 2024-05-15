""" Application """

import dash
import dash_bootstrap_components as dbc
import flask


server = flask.Flask(__name__)

app = dash.Dash(
    __name__,
    server=server,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width initial-scale=1, maximum-scale=1",
        }
    ],
    title="xarray-browser",
    update_title=None,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
    ],
)

