""" functions to handle callbacks for dynamic listing """
import os
from dash.dependencies import Input, Output, State

from pathlib import Path
from xarray_browser.server import app
from dash import html


from dash import dcc

def list_directory_contents(path):
    try:
        contents = os.listdir(path)
        dirs = sorted([item for item in contents if os.path.isdir(os.path.join(path, item))])
        files = sorted([item for item in contents if os.path.isfile(os.path.join(path, item))])
        return dirs, files
    except PermissionError:
        return [], []



def generate_directory_listing(path, open_dirs):

    dirs, files = list_directory_contents(path)

    path_parts = path.strip('/').split('/') if path.strip('/') else []
    current_path = '/'

    # Create directory breadcrumb
    breadcrumb_links = [dcc.Link('Root', href='/')]
    for part in path_parts:
        current_path = os.path.join(current_path, part)
        breadcrumb_links.append(html.Span(' / '))
        breadcrumb_links.append(dcc.Link(part, href=current_path))

    # Generate directory list items
    dir_items = []
    for dir_name in dirs:
        full_path = os.path.join(path, dir_name)
        is_open = full_path in open_dirs

        dir_items.append(html.Li([
            html.Span('[DIR] '),
            html.Span(dir_name, id={'type': 'dir-link', 'path': full_path}, style={'cursor': 'pointer'}),
            html.Ul(id={'type': 'dir-content', 'path': full_path}, style={'display': 'block' if is_open else 'none'})
        ]))

    # Generate file list items
    file_items = [html.Li(file_name) for file_name in files]

    return html.Div([
        html.H4('Directory Listing'),
        html.Div(breadcrumb_links),
        html.Ul(dir_items + file_items)
    ])


@app.callback(
    Output('dir-content', 'children'),
    [Input('dir-link',  'n_clicks')],
    [State('dir-link',  'id'),
     State('open-dirs', 'data')],
    prevent_initial_call=True
)
def toggle_directory(n_clicks, dir_id, open_dirs):
    dir_path = dir_id['path']

    if dir_path in open_dirs:
        open_dirs.remove(dir_path)
    else:
        open_dirs.append(dir_path)

    return generate_directory_listing(dir_path, open_dirs)