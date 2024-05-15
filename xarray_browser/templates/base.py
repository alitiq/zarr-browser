""" base layout """

from dash import dcc
from dash import html



def base_layout() -> html.Div:
    """provides the base layout to handle application"""
    return html.Div(
        [
            dcc.Location(id="url", refresh=True),
            html.Div(
                [
                    dcc.Store(id="login-state", storage_type="local"),
                    dcc.Store(id="customer-config", storage_type="local"),
                ]
            ),
            html.Div(id="page-content"),
            dcc.Store(id='open-dirs', data=[]),
        ],
        id="mainContainer",
    )
