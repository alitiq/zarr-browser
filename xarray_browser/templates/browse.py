
from dash import html

html.Div([
        html.H4('Directory Listing'),
        html.Div(),  # Remove the trailing ' / '
        html.Ul([
            html.Li(dcc.Link(f'[DIR] {dir_name}', href=os.path.join(pathname, dir_name)))
            for dir_name in dirs
        ]),
        html.Ul([
            html.Li(file_name)
            for file_name in files
        ])
    ])
