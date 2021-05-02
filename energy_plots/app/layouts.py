import json
from datetime import datetime

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


def fig_year(year):
    try:
        with open(f'./plots/electricity-{year}.json', 'r') as f:
            fig = json.load(f)
    except:
        fig = {}

    return fig


def fig_month(year, month):
    try:
        with open(f'./plots/electricity-{year}-{month}.json', 'r') as f:
            fig = json.load(f)
    except:
        fig = {}

    return fig


def home_layout(year=datetime.now().year, month=datetime.now().month):
    layout = dbc.Container([
        html.Div(id='test'),
        dbc.Row(html.Br()),
        dbc.Row([
            dbc.Col([
                dbc.Tabs([
                    dbc.Tab(
                        dbc.Card([
                            dbc.CardHeader(
                                dbc.DropdownMenu(
                                    id='month-tab-dropdown-year-menu',
                                    label="Year",
                                    children=[
                                        dbc.DropdownMenuItem("Item 1",
                                                             id={'type': 'month-tab-dropdown-year', 'index': 0}),
                                        dbc.DropdownMenuItem("Item 2",
                                                             id={'type': 'month-tab-dropdown-year', 'index': 1}),
                                        dbc.DropdownMenuItem("Item 3",
                                                             id={'type': 'month-tab-dropdown-year', 'index': 2}),
                                    ],
                                )
                            ),
                            dbc.CardBody(
                                [
                                    dbc.Row([
                                        dbc.Col(
                                            dbc.Button(html.Span(['navigate_before'], className="material-icons")),
                                            width=1),
                                        dbc.Col(dcc.Graph(figure=fig_month(year, month),
                                                          style={'margin-top': '10px', 'margin-bottom': '10px'})),
                                        dbc.Col(
                                            dbc.Button(html.Span(['navigate_next'], className="material-icons")),
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
                                        dbc.Col(
                                            dbc.Button(html.Span(['navigate_before'], className="material-icons")),
                                            width=1),
                                        dbc.Col(dcc.Graph(figure=fig_year(year),
                                                          style={'margin-top': '10px', 'margin-bottom': '10px'})),
                                        dbc.Col(
                                            dbc.Button(html.Span(['navigate_next'], className="material-icons")),
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

    return layout
