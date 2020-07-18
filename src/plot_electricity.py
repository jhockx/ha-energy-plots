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
daily_electricity_usage = sys.argv[5] if sys.argv[5] != 'none' else None
daily_yield = sys.argv[6] if sys.argv[6] != 'none' else None
predicted_solar = json.loads(sys.argv[7]) if sys.argv[7] != 'none' else None

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
    data = []

    if daily_electricity_usage is not None:
        df = get_df_current_month(client, daily_electricity_usage, 'kWh', now, last_day_of_the_month)
        trace1 = go.Bar(name='Verbruik totaal', x=df.index, y=df['value'], marker_color='blue')
        data.append(trace1)

    if daily_yield is not None:
        df = get_df_current_month(client, daily_yield, 'kWh', now, last_day_of_the_month)
        trace2 = go.Bar(name='Opbrengst', x=df.index, y=df['value'], marker_color='limegreen')
        data.append(trace2)

    # Build figure
    layout = {
        "yaxis": dict(title='kWh'),
        "margin": dict(l=0, r=0, t=0, b=1),
        "legend_orientation": "h"
    }
    fig = go.Figure(data=data, layout=layout)

    # Add predicted solar line
    if predicted_solar is not None:
        fig.add_shape(
            # Predicted (mean) solar horizontal line
            type="line",
            x0=first_day_of_the_month,
            y0=predicted_solar[str(now.year)][str(now.month)] / last_day_of_the_month.day,
            x1=last_day_of_the_month,
            y1=predicted_solar[str(now.year)][str(now.month)] / last_day_of_the_month.day,
            line={"color": "gray", "width": 4}
        )

    # Save figure
    fig.write_html("./src/current-month-static.html", config={'staticPlot': True})

    ##### YEARLY PLOTS #####
    # Build traces
    data = []

    if daily_electricity_usage is not None:
        df = get_df_current_year(client, daily_electricity_usage, 'kWh', now)
        trace1 = go.Bar(name='Verbruik totaal', x=df.index, y=df['value'], marker_color='blue')
        data.append(trace1)

    if daily_yield is not None:
        df = get_df_current_year(client, daily_yield, 'kWh', now)
        trace2 = go.Bar(name='Opbrengst', x=df.index, y=df['value'], marker_color='limegreen')
        data.append(trace2)

    if predicted_solar is not None:
        x_solar_predicted = [pd.to_datetime(date(now.year, int(month), 1)) for month in
                             predicted_solar[str(now.year)].keys()]
        y_solar_predicted = list(predicted_solar[str(now.year)].values())
        trace3 = go.Bar(name='Prognose', x=x_solar_predicted, y=y_solar_predicted, marker_color='gray')
        data.append(trace3)

    # Build figure
    layout = {
        "yaxis": dict(title='kWh'),
        "margin": dict(l=0, r=0, t=0, b=1),
        "legend_orientation": "h"
    }
    fig = go.Figure(data=data, layout=layout)

    # Save figure
    fig.write_html("./src/current-year-static.html", config={'staticPlot': True})

    print('End loop...')
    sleep(300)
