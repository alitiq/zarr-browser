""" callbacks to load and vis. Zarr metadata """

from dash.dependencies import Input, Output

from pathlib import Path
from zarr_browser.server import app
from dash import html
import xarray
from dask.array.svg import svg
import json
from dask.array.core import normalize_chunks
from dask.utils import format_bytes
import numpy as np
import dash_bootstrap_components as dbc


@app.callback(Output("display-xarray", "children"), [Input("url", "pathname")])
def display_xarray_html(pathname):
    """
    Display the HTML representation of an xarray dataset based on the current pathname.

    Args:
        pathname (str): The current pathname.

    Returns:
        list: A list containing a Dash Bootstrap Component card with the xarray dataset metadata and visualizations.
    """
    if pathname[-1] == "/":
        pathname = pathname[:-1]
    if ".zarr" in pathname:
        splitted_paths = pathname.split("/")

        zarr_path = Path("/")
        for sub_dir in splitted_paths:
            if ".zarr" in sub_dir:
                zarr_path = Path(zarr_path, sub_dir)
                break
            zarr_path = Path(zarr_path, sub_dir)

        dataset = xarray.open_dataset(zarr_path, engine="zarr")
        _zarray_metadata = json.load(
            open(Path(zarr_path, list(dataset.data_vars)[0], ".zarray"), "rb")
        )

        chunks = tuple(_zarray_metadata["chunks"])
        shape = tuple(_zarray_metadata["shape"])

        num_chunks_along_each_dim = [
            np.ceil(s / c).astype(int) for s, c in zip(shape, chunks)
        ]

        # Compute the total number of chunks
        total_chunks = np.prod(num_chunks_along_each_dim)

        return [
            dbc.Card(
                [
                    dbc.CardHeader(html.H4("Zarr metadata")),
                    dbc.Container(
                        [
                            dbc.Table(
                                [
                                    html.Tr(
                                        [
                                            html.Td(
                                                [
                                                    dbc.Table(
                                                        [
                                                            html.Thead(
                                                                [
                                                                    html.Tr(
                                                                        [
                                                                            html.Td(
                                                                                " "
                                                                            ),
                                                                            html.Th(
                                                                                "Array"
                                                                            ),
                                                                            html.Th(
                                                                                "Chunk"
                                                                            ),
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                            html.Tbody(
                                                                [
                                                                    html.Tr(
                                                                        [
                                                                            html.Th(
                                                                                "Bytes"
                                                                            ),
                                                                            html.Td(
                                                                                format_bytes(
                                                                                    dataset.nbytes
                                                                                )
                                                                            ),
                                                                            html.Td(
                                                                                format_bytes(
                                                                                    dataset.nbytes
                                                                                    / total_chunks
                                                                                )
                                                                            ),
                                                                        ]
                                                                    ),
                                                                    html.Tr(
                                                                        [
                                                                            html.Th(
                                                                                "Shape"
                                                                            ),
                                                                            html.Td(
                                                                                f"{shape}"
                                                                            ),
                                                                            html.Td(
                                                                                f"{chunks}"
                                                                            ),
                                                                        ]
                                                                    ),
                                                                ]
                                                            ),
                                                        ],
                                                        style={
                                                            "borderCollapse": "collapse"
                                                        },
                                                    )
                                                ]
                                            ),
                                            html.Td(
                                                html.Iframe(
                                                    srcDoc=svg(
                                                        normalize_chunks(chunks, shape),
                                                        size=250,
                                                    ),
                                                    style={
                                                        "height": "30vh",
                                                        "width": "100%",
                                                    },
                                                )
                                            ),
                                        ]
                                    )
                                ]
                            )
                        ],
                        style={"height": "30vh", "width": "100%", "margin-left": "0px"},
                    ),
                    html.Iframe(
                        srcDoc=dataset._repr_html_(),
                        style={"height": "30vh", "width": "100%"},
                    ),
                ]
            )
        ]
