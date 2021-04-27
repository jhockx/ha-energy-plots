import calendar
import json
import traceback
from datetime import datetime, date, timedelta
from time import sleep

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from influxdb import DataFrameClient

from utils import get_df_current_month, get_df_current_year, NoInfluxDataError

with open('./data/options.json', 'r') as f:
    settings = json.load(f)
settings['predicted solar'] = json.loads(settings['predicted solar'])

# Pandas DataFrame results
client = DataFrameClient(host=settings['host'], port=settings['port'],
                         username=settings['username'], password=settings['password'])

while True:
    try:
        print('Start loop plot_gas...')

        # Set variables
        now = datetime.now()
        first_day_of_the_month = pd.to_datetime(date(now.year, now.month, 1), utc=True)
        last_day_of_the_month = pd.to_datetime(date(now.year, now.month, calendar.monthrange(now.year, now.month)[1]),
                                               utc=True)

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

        if settings['daily gas usage db entity'] is not None:
            df = get_df_current_month(client, settings['daily gas usage db entity'], 'm3',
                                      first_day_of_the_month, last_day_of_the_month)
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

        ##### YEARLY PLOTS #####
        # Build traces
        data = []

        if settings['daily gas usage db entity'] is not None:
            df = get_df_current_year(client, settings['daily gas usage db entity'], 'm3', now)
            trace1 = go.Bar(name='Verbruik', x=df.index, y=df['value'], marker_color='blue')
            data.append(trace1)

        # Build figure
        fig = go.Figure(data=data, layout=layout)
        fig.update_layout(xaxis_tickformat='%b')

        # Save figure
        fig.write_html("./plots/gas-current-year-static.html", config={'staticPlot': True})

        print('End loop plot_gas...')

    except NoInfluxDataError as e:
        print(f'The database returned an empty DataFrame, this might be because it is the first of the month right '
              f'after midnight, so there is no data yet. Continuing...')
    except Exception as e:
        print(f'The following error has occurred: {e}')
        print(f'Traceback:\n{traceback.format_exc()}')
        raise

    sleep(300)
