print('Start influx script')

import calendar
import json
import sys
from datetime import datetime, date
from time import sleep

import pandas as pd
import plotly.graph_objs as go
from influxdb import DataFrameClient

from utils import get_df_current_month, get_df_current_year

# Influxdb settings
host = sys.argv[1]
port = int(sys.argv[2])
username = sys.argv[3]
password = sys.argv[4]
daily_electricity_usage = sys.argv[5]
daily_yield = sys.argv[6]
predicted_solar = json.loads(sys.argv[7])

# Pandas DataFrame results
client = DataFrameClient(host=host, port=port, username=username, password=password)

while True:
    print('Start loop...')
    now = datetime.now()
    first_day_of_the_month = pd.to_datetime(date(now.year, now.month, 1), utc=True)
    last_day_of_the_month = pd.to_datetime(date(now.year, now.month, calendar.monthrange(now.year, now.month)[1]),
                                           utc=True)

    ##### MONTHLY PLOTS #####
    # Build traces
    df = get_df_current_month(client, daily_electricity_usage, 'kWh', now, last_day_of_the_month)
    trace1 = go.Bar(name='Verbruik totaal', x=df.index, y=df['value'], marker_color='blue')
    df = get_df_current_month(client, daily_yield, 'kWh', now, last_day_of_the_month)
    trace2 = go.Bar(name='Opbrengst', x=df.index, y=df['value'], marker_color='limegreen')

    # Plotly build figure
    data = [trace1, trace2]
    layout = {
        "yaxis": dict(title='kWh'),
        "margin": dict(l=0, r=0, t=0, b=1),
        "legend_orientation": "h"
    }
    fig = go.Figure(data=data, layout=layout)
    fig.add_shape(
        # Predicted (mean) solar horizontal line
        type="line",
        x0=first_day_of_the_month,
        y0=predicted_solar[str(now.year)][str(now.month)] / last_day_of_the_month.day,
        x1=last_day_of_the_month,
        y1=predicted_solar[str(now.year)][str(now.month)] / last_day_of_the_month.day,
        line={"color": "gray", "width": 4}
    )
    fig.write_html("./src/current-month-static.html", config={'staticPlot': True})

    ##### YEARLY PLOTS #####
    # Build traces
    df = get_df_current_year(client, daily_electricity_usage, 'kWh', now)
    trace1 = go.Bar(name='Verbruik totaal', x=df.index, y=df['value'], marker_color='blue')
    df = get_df_current_year(client, daily_yield, 'kWh', now)
    trace2 = go.Bar(name='Opbrengst', x=df.index, y=df['value'], marker_color='limegreen')
    x_solar_predicted = [pd.to_datetime(date(now.year, int(month), 1)) for month in
                         predicted_solar[str(now.year)].keys()]
    y_solar_predicted = list(predicted_solar[str(now.year)].values())
    trace3 = go.Bar(name='Prognose', x=x_solar_predicted, y=y_solar_predicted, marker_color='gray')

    # Plotly build figure
    data = [trace1, trace2, trace3]
    layout = {
        "yaxis": dict(title='kWh'),
        "margin": dict(l=0, r=0, t=0, b=1),
        "legend_orientation": "h"
    }
    fig = go.Figure(data=data, layout=layout)
    fig.write_html("./src/current-year-static.html", config={'staticPlot': True})

    print('End loop...')
    sleep(300)
