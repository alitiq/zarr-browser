""" callbacks for screening root_dir and show tree"""

import os
from dash.dependencies import Input, Output, State

from pathlib import Path
from zarr_browser.server import app
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc


def list_directory_contents(path):
    """
    List the contents of a directory, separating them into directories and files.

    Args:
        path (str): The path to the directory.

    Returns:
        tuple: A tuple containing two lists:
            - dirs (list): Sorted list of directories in the specified path.
            - files (list): Sorted list of files in the specified path.

    Raises:
        PermissionError: If the directory cannot be accessed due to permission issues.
    """
    try:
        contents = os.listdir(path)
        dirs = sorted(
            [item for item in contents if os.path.isdir(os.path.join(path, item))]
        )
        files = sorted(
            [item for item in contents if os.path.isfile(os.path.join(path, item))]
        )
        return dirs, files
    except PermissionError:
        return [], []


def generate_directory_listing(path, open_dirs):
    """
    Generate the HTML representation of a directory listing.

    Args:
        path (str): The path to the directory.
        open_dirs (list): List of open directories.

    Returns:
        dbc.Card: A Dash Bootstrap Component card containing the directory listing.
    """
    dirs, files = list_directory_contents(path)

    path_parts = path.strip("/").split("/") if path.strip("/") else []
    current_path = "/"

    # Create directory breadcrumb
    breadcrumb_links = [dcc.Link("/", href="/")]
    for part in path_parts:
        current_path = Path(current_path, part)
        if len(breadcrumb_links) > 1:
            breadcrumb_links.append(html.Span(" / "))
        breadcrumb_links.append(dcc.Link(part, href=str(current_path)))

    # Generate directory list items
    dir_items = []
    for dir_name in dirs:
        full_path = os.path.join(path, dir_name)
        is_open = full_path in open_dirs

        dir_items.append(
            html.Li(
                [
                    html.Span(
                        dcc.Link(dir_name, href=full_path),
                        id={"type": "dir-link", "path": full_path},
                        style={"cursor": "pointer"},
                    ),
                    html.Ul(
                        id={"type": "dir-content", "path": full_path},
                        style={"display": "block" if is_open else "none"},
                    ),
                ]
            )
        )

    # Generate file list items
    file_items = [
        html.Li(
            html.A(
                file_name,
                href=str(Path(current_path, file_name)),
                download=str(Path(current_path, file_name)),
                style={"color": "black", "text-decoration": "none"},
            )
        )
        for file_name in files
    ]

    return dbc.Card(
        [
            dbc.CardHeader(html.H4("Directory Listing")),
            html.Div(breadcrumb_links),
            html.Ul(dir_items + file_items),
        ]
    )


@app.callback(
    Output("dir-content", "children"),
    [Input("url", "pathname")],
    [State("open-dirs", "data")],
    prevent_initial_call=True,
)
def toggle_directory(n_clicks, pathname, open_dirs):
    """
    Toggle the open/closed state of a directory in the listing.

    Args:
        n_clicks (int): Number of times the directory link has been clicked.
        pathname (str): The current pathname.
        open_dirs (list): List of currently open directories.

    Returns:
        dbc.Card: Updated directory listing.
    """
    dir_path = pathname

    if dir_path in open_dirs:
        open_dirs.remove(dir_path)
    else:
        open_dirs.append(dir_path)

    return generate_directory_listing(dir_path, open_dirs)


@app.callback(
    Output("file-system-display", "children"),
    [Input("url", "pathname")],
    [State("open-dirs", "data")],
)
def display_file_system_page(pathname, open_dirs):
    """
    Display the file system page content based on the current pathname.

    Args:
        pathname (str): The current pathname.
        open_dirs (list): List of currently open directories.

    Returns:
        dbc.Card: Directory listing for the specified pathname.
    """
    if pathname == "/" or pathname == "/browse":
        pathname = os.environ["ROOT_DIR"]
    return generate_directory_listing(pathname, open_dirs)
