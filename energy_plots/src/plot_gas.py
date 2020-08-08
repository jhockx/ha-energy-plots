import calendar
import sys
from datetime import datetime, date, timedelta
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
daily_gas_usage = sys.argv[5] if sys.argv[5] != 'none' else None
daily_gas_usage_monthly_avg = sys.argv[6].capitalize() == 'True' if sys.argv[6] != 'none' else None

# Pandas DataFrame results
client = DataFrameClient(host=host, port=port, username=username, password=password)

while True:
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

    if daily_gas_usage is not None:
        df = get_df_current_month(client, daily_gas_usage, 'm3', now, last_day_of_the_month)
        trace1 = go.Bar(name='Verbruik', x=df.index, y=df['value'], marker_color='blue')
        data.append(trace1)

    # Build figure
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(xaxis_tickformat='%d %b',
                      xaxis={'range': [first_day_of_the_month - timedelta(days=0.5),
                                       last_day_of_the_month + timedelta(days=0.5)]}
                      )

    # Add lines for monthly averages
    if daily_gas_usage_monthly_avg:
        df = get_df_current_month(client, daily_gas_usage, 'm3', now, last_day_of_the_month)
        y = df['value'].mean()
        fig.add_shape(
            # Predicted (mean) solar horizontal line
            type="line",
            x0=first_day_of_the_month - timedelta(days=1),
            y0=y,
            x1=last_day_of_the_month + timedelta(days=1),
            y1=y,
            line={"color": "blue", "width": 2, "dash": "dash"}
        )

    # Save figure
    fig.write_html("./src/gas-current-month-static.html", config={'staticPlot': True})

    ##### YEARLY PLOTS #####
    # Build traces
    data = []

    if daily_gas_usage is not None:
        df = get_df_current_year(client, daily_gas_usage, 'm3', now)
        trace1 = go.Bar(name='Verbruik', x=df.index, y=df['value'], marker_color='blue')
        data.append(trace1)

    # Build figure
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(xaxis_tickformat='%b')

    # Save figure
    fig.write_html("./src/gas-current-year-static.html", config={'staticPlot': True})

    print('End loop plot_gas...')
    sleep(300)
