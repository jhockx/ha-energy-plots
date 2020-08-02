from datetime import date

import pandas as pd


def get_df_current_month(client, entity, unit, now, last_day_of_the_month):
    # Get daily data
    result = client.query(f"SELECT entity_id, value FROM homeassistant.infinite.{unit} WHERE entity_id = '{entity}' "
                          f"AND time >= now() - 31d")
    df = result[f'{unit}']
    df = df.sort_index().resample('D').max()

    # Filter data this month
    df = df[df.index.month == now.month]

    # Add empty value on the last day of the month for the plot if it doesn't exist
    if df.empty is False and df.index[-1] != last_day_of_the_month:
        df = df.append(pd.DataFrame(index=[last_day_of_the_month], data=[[entity, 0]], columns=['entity_id', 'value']),
                       sort=True)
    return df


def get_df_current_year(client, entity, unit, now):
    # Get daily data
    result = client.query(f"SELECT entity_id, value FROM homeassistant.infinite.{unit} WHERE entity_id = '{entity}' "
                          f"AND time >= now() - 365d")
    df = result[f'{unit}']
    df = df.sort_index().resample('D').max()
    df = df.sort_index().resample('M', kind='period').sum().to_timestamp()  # returns first day on each month

    # Filter data this year
    beginning_of_current_year = pd.to_datetime(date(now.year, 1, 1))
    end_of_current_year = pd.to_datetime(date(now.year, 12, 1))
    df = df[df.index.year == now.year]
    df['entity_id'] = entity

    # # Add empty value on the first and last day of the year for the plot if it doesn't exist
    if df.empty is False and df.index[0] != beginning_of_current_year:
        df = df.append(pd.DataFrame(index=[beginning_of_current_year], data=[[entity, 0]],
                                    columns=['entity_id', 'value']), sort=True)
    if df.empty is False and df.index[-1] != end_of_current_year:
        df = df.append(pd.DataFrame(index=[end_of_current_year], data=[[entity, 0]],
                                    columns=['entity_id', 'value']), sort=True)
    df = df.sort_index()
    return df
