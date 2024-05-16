""" base layout """

import dash_bootstrap_components as dbc
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
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col([], width=5, id="file-system-display"),
                            dbc.Col([], width=7, id="display-xarray"),
                        ]
                    )
                ],
                id="page-content",
                style={
                    "margin-left": "2vh",
                    "margin-right": "2vh",
                    "margin-top": "2vh",
                },
            ),
            dcc.Store(id="open-dirs", data=[]),
        ],
        id="mainContainer",
    )
