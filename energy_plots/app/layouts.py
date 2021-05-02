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


def years_in_data(energy_type):
    with open(f'./plots/{energy_type}-years', 'r') as f:
        years_list = []

        for line in list(set(f.readlines())):
            years_list.append(int(line))

        years_list.sort(reverse=True)

    return years_list


def months_in_data(energy_type, year):
    with open(f'./plots/{energy_type}-months', 'r') as f:
        months_list = []

        for line in list(set(f.readlines())):
            if year == int(line.split('-')[0]):
                months_list.append(int(line.split('-')[1]))

        months_list.sort(reverse=True)

    return months_list


def dropdown_year_menu(energy_type, tab):
    years = years_in_data(energy_type)

    rv = []
    for index, year in enumerate(years):
        rv.append(dbc.DropdownMenuItem(year,
                                       id={
                                           'type': f'dropdown-year',
                                           'index': index,
                                           'energy_type': energy_type,
                                           'tab': tab
                                       }))

    return rv


def electricity_layout(year=datetime.now().year, month=datetime.now().month):
    layout = dbc.Container([
        dbc.Row(html.Br()),
        dbc.Row([
            dbc.Col([
                dbc.Tabs([
                    dbc.Tab(
                        dbc.Card([
                            dbc.CardHeader(
                                dbc.DropdownMenu(
                                    id={'type': 'dropdown-year-menu', 'energy_type': 'electricity', 'tab': 'month'},
                                    label="Year",
                                    children=dropdown_year_menu('electricity', 'month'),
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
                        dbc.Card([
                            dbc.CardHeader(
                                dbc.DropdownMenu(
                                    id={'type': 'dropdown-year-menu', 'energy_type': 'electricity', 'tab': 'year'},
                                    label="Year",
                                    children=dropdown_year_menu('electricity', 'year'),
                                )
                            ),
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
                            )],
                            className="mt-3"
                        )
                        , label="Year"),
                ]
                )
            ])
        ])
    ])

    return layout
