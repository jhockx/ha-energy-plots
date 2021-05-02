import json

from dash import callback_context
from dash.dependencies import Input, Output, State, ALL, MATCH

from app import app


@app.callback(
    Output({'type': 'dropdown-year-menu', 'energy_type': MATCH, 'tab': MATCH}, 'label'),
    Input({'type': 'dropdown-year', 'index': ALL, 'energy_type': MATCH, 'tab': MATCH}, 'n_clicks'),
    [
        State({'type': 'dropdown-year', 'index': ALL, 'energy_type': MATCH, 'tab': MATCH}, 'children'),
        State({'type': 'dropdown-year-menu', 'energy_type': MATCH, 'tab': MATCH}, 'label')
    ]
)
def dropdown_click(n_clicks, children, label):
    app.logger.info(callback_context.triggered[0])
    prop_id = callback_context.triggered[0]['prop_id']
    index = json.loads(prop_id.rstrip('.n_clicks'))['index'] if prop_id != '.' else None

    return list(children)[index] if index is not None else label
