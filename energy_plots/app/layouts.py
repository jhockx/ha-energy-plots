import json

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

try:
    with open('./plots/electricity-2021.json', 'r') as f:
        fig_year = json.load(f)
except:
    fig_year = {}

try:
    with open('./plots/electricity-2021-4.json', 'r') as f:
        fig_month = json.load(f)
except:
    fig_month = {}

home_layout = dbc.Container([
    dbc.Row(html.Br()),
    dbc.Row([
        dbc.Col([
            dbc.Tabs([
                dbc.Tab(
                    dbc.Card([
                        dbc.CardBody(
                            [
                                dbc.Row([
                                    dbc.Col(dbc.Button(html.Span(['navigate_before'], className="material-icons")),
                                            width=1),
                                    dbc.Col(dcc.Graph(figure=fig_month,
                                                      style={'margin-top': '10px', 'margin-bottom': '10px'})),
                                    dbc.Col(dbc.Button(html.Span(['navigate_next'], className="material-icons")),
                                            width=1)
                                ], align="center")
                            ]
                        )],
                        className="mt-3"
                    )
                    , label="Month"),
                dbc.Tab(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row([
                                    dbc.Col(dbc.Button(html.Span(['navigate_before'], className="material-icons")),
                                            width=1),
                                    dbc.Col(dcc.Graph(figure=fig_year,
                                                      style={'margin-top': '10px', 'margin-bottom': '10px'})),
                                    dbc.Col(dbc.Button(html.Span(['navigate_next'], className="material-icons")),
                                            width=1)
                                ], align="center")
                            ]
                        ),
                        className="mt-3"
                    )
                    , label="Year"),
            ]
            )
        ])
    ])
])
