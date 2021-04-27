from datetime import timedelta

import numpy as np
import pandas as pd
import plotly.graph_objs as go

from utils import get_first_and_last_day_of_the_month, get_df_current_month, get_df_current_year


def make_gas_plots(settings, client, now):
    # Set variables
    first_day_of_the_month, last_day_of_the_month = get_first_and_last_day_of_the_month(now)

    # Set layout for all plots
    layout = {
        "yaxis": dict(title='m3'),
        "margin": dict(l=0, r=0, t=0, b=20),
        "legend_orientation": "h",
        "showlegend": True
    }

    ##### MONTHLY PLOTS #####
    # Build traces
    data = []

    if settings.get('daily gas usage db entity'):
        df = get_df_current_month(client, settings['daily gas usage db entity'], settings['db_unit_prefix'],
                                  settings['db_unit_suffix'], 'm3', now)
        # Fill missing rows with zero
        df = df.resample('D').max().fillna(0)
        trace = go.Bar(name='Verbruik', x=df.index, y=df['value'], marker_color='blue')
        data.append(trace)
        if settings['plot average gas usage']:
            y = df['value'].replace(0, np.nan).mean()
            df = pd.DataFrame(data=[[first_day_of_the_month - timedelta(days=1), y],
                                    [last_day_of_the_month + timedelta(days=1), y]],
                              columns=['date', 'value'])
            trace = go.Scatter(name='Gem. verbruik', x=df['date'], y=df['value'], mode='lines',
                               marker_color='blue', line={'width': 2, "dash": "dash"})
            data.append(trace)

    # Build figure
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(xaxis_tickformat='%d %b',
                      xaxis={'range': [first_day_of_the_month - timedelta(days=0.5),
                                       last_day_of_the_month + timedelta(days=0.5)]}
                      )

    # Save figure
    fig.write_html("./plots/gas-current-month-static.html", config={'staticPlot': True})
    fig.write_html(f"./plots/gas-{now.year}-{now.month}.html")

    ##### YEARLY PLOTS #####
    # Build traces
    data = []

    if settings.get('daily gas usage db entity'):
        df = get_df_current_year(client, settings['daily gas usage db entity'], settings['db_unit_prefix'],
                                 settings['db_unit_suffix'], 'm3', now)
        trace1 = go.Bar(name='Verbruik', x=df.index, y=df['value'], marker_color='blue')
        data.append(trace1)

    # Build figure
    fig = go.Figure(data=data, layout=layout)
    fig.layout.xaxis.tickvals = pd.date_range(f'{now.year}-01', f'{now.year}-12', freq='MS')
    fig.update_layout(xaxis_tickformat='%b', bargap=0.2)

    # Save figure
    fig.write_html("./plots/gas-current-year-static.html", config={'staticPlot': True})
    fig.write_html(f"./plots/gas-{now.year}.html")
