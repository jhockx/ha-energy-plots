import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from configs import dash_config

skeleton_layout = html.Div([
    # Routing
    # https://dash.plotly.com/urls
    dcc.Location(id='url', refresh=False),

    # Navbar
    # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/
    dbc.NavbarSimple(
        brand=f'{dash_config.TITLE}',
        color='primary',
        dark=True,
        children=[dbc.NavItem(dbc.NavLink(route['name'], href=route['url'])) for route in dash_config.ROUTES]
    ),

    # Routing
    # https://dash.plotly.com/urls
    html.Div(id='page-content')
])

home_layout = dbc.Row([
    dbc.Col([
        html.H3('Test')
    ])
])
