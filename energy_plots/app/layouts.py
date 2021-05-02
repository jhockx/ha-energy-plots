import json
from datetime import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from configs import dash_config


##### HELPER METHODS #####
def fig_year(year, energy_type):
    try:
        with open(f'./plots/{energy_type}-{year}.json', 'r') as f:
            fig = json.load(f)
    except:
        fig = {}

    return fig


def fig_month(year, month, energy_type):
    try:
        with open(f'./plots/{energy_type}-{year}-{month}.json', 'r') as f:
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


def dropdown_month_menu(energy_type, tab, year):
    months = months_in_data(energy_type, year)

    rv = []
    for index, month in enumerate(months):
        rv.append(dbc.DropdownMenuItem(month,
                                       id={
                                           'type': f'dropdown-month',
                                           'index': index,
                                           'energy_type': energy_type,
                                           'tab': tab
                                       }))

    return rv


def energy_layout(year, month, energy_type):
    layout = dbc.Container([
        dbc.Row(dbc.Col(html.H4(energy_type.capitalize()), style={'margin-top': '1em'})),
        dbc.Row([
            dbc.Col([
                dbc.Tabs([
                    dbc.Tab(
                        dbc.Card([
                            dbc.CardHeader([
                                dbc.Row([
                                    dbc.Col(
                                        dbc.DropdownMenu(
                                            id={'type': 'dropdown-year-menu', 'energy_type': energy_type,
                                                'tab': 'month'},
                                            label="Year",
                                            children=dropdown_year_menu(energy_type, 'month'),
                                        ),
                                        width=1
                                    ),
                                    dbc.Col(
                                        dbc.DropdownMenu(
                                            id={'type': 'dropdown-month-menu', 'energy_type': energy_type,
                                                'tab': 'month'},
                                            label="Month",
                                            children=[],
                                            disabled=True
                                        ),
                                        width=1
                                    )
                                ])
                            ]),
                            dbc.CardBody(
                                [
                                    dbc.Row([
                                        dbc.Col(
                                            dbc.Button(html.Span(['navigate_before'], className="material-icons")),
                                            width=1),
                                        dbc.Col(
                                            dcc.Graph(
                                                id={'type': 'figure',
                                                    'energy_type': energy_type,
                                                    'tab': 'month'},
                                                figure=fig_month(year, month, energy_type),
                                                style={'margin-top': '1em', 'margin-bottom': '1em'}
                                            )
                                        ),
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
                            dbc.CardHeader([
                                dbc.DropdownMenu(
                                    id={'type': 'dropdown-year-menu', 'energy_type': energy_type, 'tab': 'year'},
                                    label="Year",
                                    children=dropdown_year_menu(energy_type, 'year'),
                                ),
                                dbc.DropdownMenu(
                                    id={'type': 'dropdown-month-menu', 'energy_type': energy_type, 'tab': 'year'},
                                    label="Month",
                                    children=[],
                                    disabled=True,
                                    style={'display': 'none'}
                                )
                            ]),
                            dbc.CardBody(
                                [
                                    dbc.Row([
                                        dbc.Col(
                                            dbc.Button(html.Span(['navigate_before'], className="material-icons")),
                                            width=1),
                                        dbc.Col(
                                            dcc.Graph(
                                                id={'type': 'figure',
                                                    'energy_type': energy_type,
                                                    'tab': 'year'},
                                                figure=fig_year(year, energy_type),
                                                style={'margin-top': '10px', 'margin-bottom': '10px'}
                                            )
                                        ),
                                        dbc.Col(
                                            dbc.Button(html.Span(['navigate_next'], className="material-icons")),
                                            width=1)
                                    ], align="center")
                                ]
                            )],
                            className="mt-3"
                        )
                        , label="Year"),
                ])
            ])
        ]),
        dbc.Row(html.Br())
    ])

    return layout


##### LAYOUTS #####
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


def electricity_layout(year=datetime.now().year, month=datetime.now().month):
    return energy_layout(year, month, 'electricity')


def gas_layout(year=datetime.now().year, month=datetime.now().month):
    return energy_layout(year, month, 'gas')
