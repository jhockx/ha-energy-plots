import calendar
import json
import sys
import traceback
from datetime import datetime, date, timedelta
from time import sleep

import pandas as pd
import plotly.graph_objs as go
from influxdb import DataFrameClient

from utils import get_df_current_month, get_df_current_year, NoInfluxDataError

# Influxdb settings
host = sys.argv[1]
port = int(sys.argv[2])
username = sys.argv[3]
password = sys.argv[4]
daily_electricity_usage = sys.argv[5] if sys.argv[5] != 'none' else None
daily_yield = sys.argv[6] if sys.argv[6] != 'none' else None
daily_electricity_usage_monthly_avg = sys.argv[7].capitalize() == 'True' if sys.argv[7] != 'none' else None
daily_yield_monthly_avg = sys.argv[8].capitalize() == 'True' if sys.argv[8] != 'none' else None
predicted_solar = json.loads(sys.argv[9]) if sys.argv[9] != 'none' else None

# Pandas DataFrame results
client = DataFrameClient(host=host, port=port, username=username, password=password)

while True:
    try:
        print('Start loop plot_electricity...')

        # Set variables
        now = datetime.now()
        first_day_of_the_month = pd.to_datetime(date(now.year, now.month, 1), utc=True)
        last_day_of_the_month = pd.to_datetime(date(now.year, now.month, calendar.monthrange(now.year, now.month)[1]),
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

        if daily_electricity_usage is not None:
            df = get_df_current_month(client, daily_electricity_usage, 'kWh', first_day_of_the_month,
                                      last_day_of_the_month)
            # Fill missing rows with zero
            df = df.resample('D').max().fillna(0)
            trace = go.Bar(name='Verbruik', x=df.index, y=df['value'], marker_color='blue')
            data.append(trace)
            if daily_electricity_usage_monthly_avg:
                y = df['value'].replace(0, pd.np.nan).mean()
                df = pd.DataFrame(data=[[first_day_of_the_month - timedelta(days=1), y],
                                        [last_day_of_the_month + timedelta(days=1), y]],
                                  columns=['date', 'value'])
                trace = go.Scatter(name='Gem. verbruik', x=df['date'], y=df['value'], mode='lines',
                                   marker_color='blue', line={'width': 2, "dash": "dash"})
                data.append(trace)

        if daily_yield is not None:
            df = get_df_current_month(client, daily_yield, 'kWh', first_day_of_the_month, last_day_of_the_month)
            # Fill missing rows with zero
            df = df.resample('D').max().fillna(0)
            trace = go.Bar(name='Opbrengst', x=df.index, y=df['value'], marker_color='limegreen')
            data.append(trace)
            if daily_yield_monthly_avg:
                y = df['value'].replace(0, pd.np.nan).mean()
                df = pd.DataFrame(data=[[first_day_of_the_month - timedelta(days=1), y],
                                        [last_day_of_the_month + timedelta(days=1), y]],
                                  columns=['date', 'value'])
                trace = go.Scatter(name='Gem. opbrengst', x=df['date'], y=df['value'], mode='lines',
                                   marker_color='limegreen', line={'width': 2, "dash": "dash"})
                data.append(trace)

        if predicted_solar is not None:
            predicted_solar_monthly_avg = predicted_solar[str(now.year)][str(now.month)] / last_day_of_the_month.day
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
        fig.write_html("./src/electricity-current-month-static.html", config={'staticPlot': True})

        ##### YEARLY PLOTS #####
        # Build traces
        data = []

        if daily_electricity_usage is not None:
            df = get_df_current_year(client, daily_electricity_usage, 'kWh', now)
            trace1 = go.Bar(name='Verbruik', x=df.index, y=df['value'], marker_color='blue')
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
        fig = go.Figure(data=data, layout=layout)
        fig.update_layout(xaxis_tickformat='%b')

        # Save figure
        fig.write_html("./src/electricity-current-year-static.html", config={'staticPlot': True})

        print('End loop plot_electricity...')

    except NoInfluxDataError as e:
        print(f'The database returned an empty DataFrame, this might be because it is the first of the month right '
              f'after midnight, so there is no data yet. Continuing...')
    except Exception as e:
        print(f'The following error has occurred: {e}')
        print(f'Traceback:\n{traceback.format_exc()}')
        raise

    sleep(300)
