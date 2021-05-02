import json

from dash import callback_context
from dash.dependencies import Input, Output, State, ALL

from app import app


@app.callback(
    Output('month-tab-dropdown-year-menu', 'label'),
    Input({'type': 'month-tab-dropdown-year', 'index': ALL}, 'n_clicks'),
    [
        State({'type': 'month-tab-dropdown-year', 'index': ALL}, 'children'),
        State('month-tab-dropdown-year-menu', 'label')
    ]
)
def dropdown_click(n_clicks, children, label):
    prop_id = callback_context.triggered[0]['prop_id']
    index = json.loads(prop_id.rstrip('.n_clicks'))['index'] if prop_id != '.' else None

    return list(children)[index] if index is not None else label
