import json

from dash import callback_context
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash.exceptions import PreventUpdate

from app import app
from app.layouts import dropdown_month_menu, fig_month, fig_year


@app.callback(
    [
        Output({'type': 'dropdown-year-menu', 'energy_type': MATCH, 'tab': MATCH}, 'label'),
        Output({'type': 'dropdown-month-menu', 'energy_type': MATCH, 'tab': MATCH}, 'children'),
        Output({'type': 'dropdown-month-menu', 'energy_type': MATCH, 'tab': MATCH}, 'disabled')
    ],
    Input({'type': 'dropdown-year', 'index': ALL, 'energy_type': MATCH, 'tab': MATCH}, 'n_clicks'),
    [
        State({'type': 'dropdown-year', 'index': ALL, 'energy_type': MATCH, 'tab': MATCH}, 'children'),
        State({'type': 'dropdown-year-menu', 'energy_type': MATCH, 'tab': MATCH}, 'label')
    ]
)
def dropdown_year_click(n_clicks, children, label_year):
    app.logger.info('Dropdown for year was clicked, processing callback')

    clicked_element = None
    prop_id = callback_context.triggered[0]['prop_id']
    if prop_id != '.' and n_clicks.count(None) != len(n_clicks):
        clicked_element = json.loads(prop_id.rstrip('.n_clicks'))

    label_year = list(children)[clicked_element['index']] if clicked_element is not None else label_year
    if label_year != 'Year':
        months_dropdown_menu_items = dropdown_month_menu(
            clicked_element['energy_type'],
            clicked_element['tab'],
            int(label_year)
        )
        months_dropdown_menu_disabled = False
    else:
        months_dropdown_menu_items = []
        months_dropdown_menu_disabled = True

    app.logger.info('Done processing callback')
    return label_year, months_dropdown_menu_items, months_dropdown_menu_disabled


@app.callback(
    Output({'type': 'dropdown-month-menu', 'energy_type': MATCH, 'tab': MATCH}, 'label'),
    Input({'type': 'dropdown-month', 'index': ALL, 'energy_type': MATCH, 'tab': MATCH}, 'n_clicks'),
    [
        State({'type': 'dropdown-month', 'index': ALL, 'energy_type': MATCH, 'tab': MATCH}, 'children'),
        State({'type': 'dropdown-month-menu', 'energy_type': MATCH, 'tab': MATCH}, 'label')
    ]
)
def dropdown_month_click(n_clicks, children, label_month):
    app.logger.info('Dropdown for month was clicked, processing callback')

    clicked_element = None
    prop_id = callback_context.triggered[0]['prop_id']
    if prop_id != '.' and n_clicks.count(None) != len(n_clicks):
        clicked_element = json.loads(prop_id.rstrip('.n_clicks'))

    label_month = list(children)[clicked_element['index']] if clicked_element is not None else label_month

    app.logger.info('Done processing callback')
    return label_month


@app.callback(
    Output({'type': 'figure', 'energy_type': MATCH, 'tab': MATCH}, 'figure'),
    [
        Input({'type': 'dropdown-month-menu', 'energy_type': MATCH, 'tab': MATCH}, 'label'),
        Input({'type': 'dropdown-year-menu', 'energy_type': MATCH, 'tab': MATCH}, 'label')
    ]
)
def dropdown_labels_changed(label_month, label_year):
    app.logger.info('Dropdown labels have changed, processing callback')

    triggered_items = []
    if label_year != 'Year':
        for item in callback_context.triggered:
            triggered_items.append(json.loads(item['prop_id'].rstrip('.label')))

    if triggered_items:
        tab = triggered_items[0]['tab']
        energy_type = triggered_items[0]['energy_type']

        if tab == 'month' and label_year != 'Year' and label_month != 'Month':
            app.logger.info('Done processing callback')
            return fig_month(int(label_year), int(label_month), energy_type)
        elif tab == 'year' and label_year != 'Year':
            app.logger.info('Done processing callback')
            return fig_year(int(label_year), energy_type)

    app.logger.info('Done processing callback')
    raise PreventUpdate
