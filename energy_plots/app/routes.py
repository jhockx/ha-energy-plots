from dash.dependencies import Input, Output

from app import app
from app.layouts import *


# Routing
# https://dash.plotly.com/urls
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    """
    This method is like the one in the documentation, except the routing is defined in the config instead of directly
    in this method, to have everything configurable in one place.
    """
    app.logger.info(f'Page requested: {pathname}')

    for route in app.server.config['ROUTES']:
        # Reroute home page (doesn't change the url)
        if pathname == '/' or pathname == app.server.config['base_url']:
            pathname = '/electricity'

        if pathname == route['url']:
            # The layout objects are imported in the top of the script and are thus globals.
            # Here it is determined which layout is going to be returned
            return globals()[route['layout']]()

    return '404 - Page not found'
