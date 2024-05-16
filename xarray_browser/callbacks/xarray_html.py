import os
from dash.dependencies import Input, Output, State

from pathlib import Path
from xarray_browser.server import app
from dash import html
import xarray
from dask.array.svg import svg
import json
from dask.array.core import normalize_chunks
from dask.utils import format_bytes
import numpy as np

table_template = """
<table>
    <tr>
        <td>
            <table style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <td> </td>
                        <th> Array </th>
                        <th> Chunk </th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <th> Bytes </th>
                        <td> {nbytes} </td>
                        <td> {cbytes} </td>
                    </tr>
                    <tr>
                        <th> Shape </th>
                        <td> {shape} </td>
                        <td> {chunksize} </td>
                    </tr>

                </tbody>
            </table>
        </td>
        <td>
        {grid}
        </td>
    </tr>
</table>
"""
unused = """
                    <tr>
                        <th> Dask graph </th>
                        <td colspan="2"> {{ array.npartitions }} chunks in {{ layers }} </td>
                    </tr>
                    <tr>
                        <th> Data type </th>
                        <td colspan="2"> {{ array.dtype }} {{ array._meta | type | typename }} </td>
                    </tr>
"""
@app.callback(Output("display-xarray", "children"),
              [Input("url", "pathname")])
def display_xarray_html(pathname):
    """main window content handler"""
    if pathname[-1] == '/':
        pathname = pathname[:-1]
    if 'zarr' == pathname[-4:]:
        dataset = xarray.open_dataset(pathname, engine='zarr')
        _zarray_metadata = json.load(open(Path(pathname, list(dataset.data_vars)[0], '.zarray'), 'rb'))

        chunks = tuple(_zarray_metadata['chunks'])
        shape = tuple(_zarray_metadata['shape'])

        num_chunks_along_each_dim = [np.ceil(s / c).astype(int) for s, c in zip(shape, chunks)]

        # Compute the total number of chunks
        total_chunks = np.prod(num_chunks_along_each_dim)

        table = table_template.format(
            shape=shape,
            chunksize=chunks,
            grid=svg(normalize_chunks(chunks, shape), size=300),
            nbytes=format_bytes(dataset.nbytes),
            cbytes=format_bytes(dataset.nbytes / total_chunks),
        )
        return [
            html.Iframe(srcDoc=table, style={'height': '30vh', 'width': '100%'}),
            html.Iframe(srcDoc=dataset._repr_html_(), style={'height': '30vh', 'width': '100%'}),
        ]