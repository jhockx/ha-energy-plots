from dash.dependencies import Input, Output

from app import app
from app.layouts import home_layout


# Routing
# https://dash.plotly.com/urls
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    """
    This method is like the one in the documentation, except the routing is defined in the config instead of directly
    in this method, to have everything configurable in one place.
    """

    if pathname == '/':
        return home_layout()

    return '404'
