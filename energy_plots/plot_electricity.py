import calendar
import json
import traceback
from datetime import timedelta, datetime
from time import sleep

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from influxdb import DataFrameClient

from utils import get_df_current_month, get_df_current_year, NoInfluxDataError

with open('./data/options.json', 'r') as f:
    settings = json.load(f)
settings['predicted solar'] = json.loads(settings['predicted solar'])


def make_plots(now):
    # Set variables
    first_day_of_the_month = pd.to_datetime(now.strftime('%Y-%m-01'), utc=True)
    last_day_of_the_month = pd.to_datetime(now.strftime(f'%Y-%m-{calendar.monthrange(now.year, now.month)[1]}'),
                                           utc=True)

    # Set layout for all plots
    layout = {
        "yaxis": dict(title='kWh'),
        "margin": dict(l=0, r=0, t=0, b=20),
        "legend_orientation": "h"
    }

    ##### MONTHLY PLOTS #####
    # Build traces
    data = []

    if settings['daily electricity usage db entity'] is not None:
        df = get_df_current_month(client, settings['daily electricity usage db entity'], 'kWh', first_day_of_the_month,
                                  last_day_of_the_month)
        # Fill missing rows with zero
        df = df.resample('D').max().fillna(0)
        trace = go.Bar(name='Verbruik', x=df.index, y=df['value'], marker_color='blue')
        data.append(trace)
        if bool(settings['plot average electricity usage']):
            y = df['value'].replace(0, np.nan).mean()
            df = pd.DataFrame(data=[[first_day_of_the_month - timedelta(days=1), y],
                                    [last_day_of_the_month + timedelta(days=1), y]],
                              columns=['date', 'value'])
            trace = go.Scatter(name='Gem. verbruik', x=df['date'], y=df['value'], mode='lines',
                               marker_color='blue', line={'width': 2, "dash": "dash"})
            data.append(trace)

    if settings['daily yield db entity'] is not None:
        df = get_df_current_month(client, settings['daily yield db entity'], 'kWh', first_day_of_the_month,
                                  last_day_of_the_month)
        # Fill missing rows with zero
        df = df.resample('D').max().fillna(0)
        trace = go.Bar(name='Opbrengst', x=df.index, y=df['value'], marker_color='limegreen')
        data.append(trace)
        if settings['plot average yield']:
            y = df['value'].replace(0, np.nan).mean()
            df = pd.DataFrame(data=[[first_day_of_the_month - timedelta(days=1), y],
                                    [last_day_of_the_month + timedelta(days=1), y]],
                              columns=['date', 'value'])
            trace = go.Scatter(name='Gem. opbrengst', x=df['date'], y=df['value'], mode='lines',
                               marker_color='limegreen', line={'width': 2, "dash": "dash"})
            data.append(trace)

    if settings['predicted solar'] is not None:
        predicted_solar_monthly_avg = settings['predicted solar'][str(now.year)][
                                          str(now.month)] / last_day_of_the_month.day
        df = pd.DataFrame(data=[[first_day_of_the_month - timedelta(days=1), predicted_solar_monthly_avg],
                                [last_day_of_the_month + timedelta(days=1), predicted_solar_monthly_avg]],
                          columns=['date', 'value'])
        trace = go.Scatter(name='Prognose', x=df['date'], y=df['value'], mode='lines',
                           marker_color='gray', line={'width': 4})
        data.append(trace)

    # Build figure
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(xaxis_tickformat='%d %b',
                      xaxis={'range': [first_day_of_the_month - timedelta(days=0.5),
                                       last_day_of_the_month + timedelta(days=0.5)]})

    # Save figure
    fig.write_html("./plots/electricity-current-month-static.html", config={'staticPlot': True})

    ##### YEARLY PLOTS #####
    # Build traces
    data = []

    if settings['daily electricity usage db entity'] is not None:
        df = get_df_current_year(client, settings['daily electricity usage db entity'], 'kWh', now)
        trace1 = go.Bar(name='Verbruik', x=df.index, y=df['value'], marker_color='blue')
        data.append(trace1)

    if settings['daily yield db entity'] is not None:
        df = get_df_current_year(client, settings['daily yield db entity'], 'kWh', now)
        trace2 = go.Bar(name='Opbrengst', x=df.index, y=df['value'], marker_color='limegreen')
        data.append(trace2)

    if settings['predicted solar'] is not None:
        x_solar_predicted = [pd.to_datetime(now.strftime(f'%Y-{month}-01')) for month in
                             settings['predicted solar'][str(now.year)].keys()]
        y_solar_predicted = list(settings['predicted solar'][str(now.year)].values())
        trace3 = go.Bar(name='Prognose', x=x_solar_predicted, y=y_solar_predicted, marker_color='gray')
        data.append(trace3)

    # Build figure
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(xaxis_tickformat='%b')

    # Save figure
    fig.write_html("./plots/electricity-current-year-static.html", config={'staticPlot': True})


# Pandas DataFrame query results
client = DataFrameClient(host=settings['host'], port=settings['port'],
                         username=settings['username'], password=settings['password'])

while True:
    try:
        print('Start loop plot_electricity...')

        now = datetime.now()
        make_plots(now)

        print('End loop plot_electricity...')

    except NoInfluxDataError as e:
        print(f'The database returned an empty DataFrame, this might be because it is the first of the month right '
              f'after midnight, so there is no data yet. Continuing...')
    except Exception as e:
        print(f'The following error has occurred: {e}')
        print(f'Traceback:\n{traceback.format_exc()}')
        raise

    sleep(300)
