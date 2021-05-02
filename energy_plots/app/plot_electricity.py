from datetime import timedelta

import numpy as np
import pandas as pd
import plotly.graph_objs as go

from app.utils import get_df_current_month, get_df_current_year, get_first_and_last_day_of_the_month


def make_electricity_plots(settings, client, now):
    # Set variables
    first_day_of_the_month, last_day_of_the_month = get_first_and_last_day_of_the_month(now)

    # Set layout for all plots
    layout = {
        "yaxis": dict(title='kWh'),
        "margin": dict(l=0, r=0, t=0, b=20),
        "legend_orientation": "h",
        "showlegend": True
    }

    ##### MONTHLY PLOTS #####
    # Build traces
    data = []

    if settings.get('daily electricity usage db entity'):
        df = get_df_current_month(client, settings['daily electricity usage db entity'], settings['db_unit_prefix'],
                                  settings['db_unit_suffix'], 'kWh', now)
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

    if settings.get('daily yield db entity'):
        df = get_df_current_month(client, settings['daily yield db entity'], settings['db_unit_prefix'],
                                  settings['db_unit_suffix'], 'kWh', now)
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

    if settings.get('predicted solar'):
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
    with open(f"./plots/electricity-{now.year}-{now.month}.json", 'w') as f:
        f.write(fig.to_json())
    with open("./plots/electricity-months", 'a') as f:
        f.write(f'{now.year}-{now.month}\n')

    ##### YEARLY PLOTS #####
    # Build traces
    data = []

    if settings.get('daily electricity usage db entity'):
        df = get_df_current_year(client, settings['daily electricity usage db entity'], settings['db_unit_prefix'],
                                 settings['db_unit_suffix'], 'kWh', now)
        trace1 = go.Bar(name='Verbruik', x=df.index, y=df['value'], marker_color='blue')
        data.append(trace1)

    if settings.get('daily yield db entity'):
        df = get_df_current_year(client, settings['daily yield db entity'], settings['db_unit_prefix'],
                                 settings['db_unit_suffix'], 'kWh', now)
        trace2 = go.Bar(name='Opbrengst', x=df.index, y=df['value'], marker_color='limegreen')
        data.append(trace2)

    if settings.get('predicted solar'):
        x_solar_predicted = [pd.to_datetime(now.strftime(f'%Y-{month}-01')) for month in
                             settings['predicted solar'][str(now.year)].keys()]
        y_solar_predicted = list(settings['predicted solar'][str(now.year)].values())
        trace3 = go.Bar(name='Prognose', x=x_solar_predicted, y=y_solar_predicted, marker_color='gray')
        data.append(trace3)

    # Build figure
    fig = go.Figure(data=data, layout=layout)
    fig.layout.xaxis.tickvals = pd.date_range(f'{now.year}-01', f'{now.year}-12', freq='MS')
    fig.update_layout(xaxis_tickformat='%b', bargap=0.2)

    # Save figure
    fig.write_html("./plots/electricity-current-year-static.html", config={'staticPlot': True})
    with open(f"./plots/electricity-{now.year}.json", 'w') as f:
        f.write(fig.to_json())
    with open("./plots/electricity-years", 'a') as f:
        f.write(f'{now.year}\n')
