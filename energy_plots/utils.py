import calendar

import pandas as pd


class NoInfluxDataError(Exception):
    pass


def get_min_max_datetimes_from_db(client, entity, db_prefix, db_suffix, unit, min_datetime, max_datetime):
    # Overwrite min_datetime if smaller value is found in the database
    query = f"""
    SELECT value FROM "homeassistant"."infinite"."{db_prefix}{unit}{db_suffix}" 
    WHERE entity_id = '{entity}' 
    LIMIT 1
    """
    result = client.query(query)
    if not result:
        raise NoInfluxDataError
    if pd.to_datetime(result[f"{db_prefix}{unit}{db_suffix}"].index[0]) < min_datetime:
        min_datetime = pd.to_datetime(result[f"{db_prefix}{unit}{db_suffix}"].index[0])

    # Overwrite max_datetime if smaller value is found in the database
    query = f"""
    SELECT value FROM "homeassistant"."infinite"."{db_prefix}{unit}{db_suffix}" 
    WHERE entity_id = '{entity}' 
    ORDER BY time DESC
    LIMIT 1
    """
    result = client.query(query)
    if not result:
        raise NoInfluxDataError
    if pd.to_datetime(result[f"{db_prefix}{unit}{db_suffix}"].index[0]) > max_datetime:
        max_datetime = pd.to_datetime(result[f"{db_prefix}{unit}{db_suffix}"].index[0])

    return min_datetime, max_datetime


def get_first_and_last_day_of_the_month(now):
    # Set variables
    first_day_of_the_month = pd.to_datetime(now.strftime('%Y-%m-01'), utc=True)
    last_day_of_the_month = pd.to_datetime(now.strftime(f'%Y-%m-{calendar.monthrange(now.year, now.month)[1]}'),
                                           utc=True)

    return first_day_of_the_month, last_day_of_the_month


def get_df_current_month(client, entity, db_prefix, db_suffix, unit, now):
    first_day_of_the_month, last_day_of_the_month = get_first_and_last_day_of_the_month(now)

    # Get daily data
    query = f"""
    SELECT entity_id, value 
    FROM "homeassistant"."infinite"."{db_prefix}{unit}{db_suffix}" 
    WHERE entity_id = '{entity}' 
    AND time >= '{first_day_of_the_month.strftime('%Y-%m-%dT%H:%M:%SZ')}'
    AND time <= '{last_day_of_the_month.strftime('%Y-%m-%dT%H:%M:%SZ')}'
    """
    result = client.query(query)
    if not result:
        raise NoInfluxDataError

    df = result[f"{db_prefix}{unit}{db_suffix}"]
    df = df.sort_index().resample('D').max()

    # Add empty value on the last day of the month for the plot if it doesn't exist
    if df.empty is False and df.index[-1] != last_day_of_the_month:
        df = df.append(pd.DataFrame(index=[last_day_of_the_month], data=[[entity, 0]], columns=['entity_id', 'value']),
                       sort=True)
    return df


def get_first_and_last_day_of_the_year(now):
    # Set variables
    first_day_of_the_year = pd.to_datetime(now.strftime('%Y-01-01'), utc=True)
    last_day_of_the_year = pd.to_datetime(now.strftime(f'%Y-12-31'), utc=True)

    return first_day_of_the_year, last_day_of_the_year


def get_df_current_year(client, entity, db_prefix, db_suffix, unit, now):
    first_day_of_the_year, last_day_of_the_year = get_first_and_last_day_of_the_year(now)

    # Get daily data
    query = f"""
    SELECT entity_id, value 
    FROM "homeassistant"."infinite"."{db_prefix}{unit}{db_suffix}" 
    WHERE entity_id = '{entity}' 
    AND time >= '{first_day_of_the_year.strftime('%Y-%m-%dT%H:%M:%SZ')}'
    AND time <= '{last_day_of_the_year.strftime('%Y-%m-%dT%H:%M:%SZ')}'
    """
    result = client.query(query)
    if not result:
        raise NoInfluxDataError

    df = result[f"{db_prefix}{unit}{db_suffix}"]
    df = df.sort_index().resample('D').max()
    df = df.sort_index().resample('M', kind='period').sum().to_timestamp()  # returns first day on each month
    df['entity_id'] = entity
    df = df.tz_localize('utc')

    # Add empty value on the first and last day of the year for the plot if it doesn't exist
    if df.empty is False and df.index[0] != first_day_of_the_year:
        df = df.append(pd.DataFrame(index=[first_day_of_the_year], data=[[entity, 0]],
                                    columns=['entity_id', 'value']), sort=True)
    if df.empty is False and df.index[-1] != last_day_of_the_year:
        df = df.append(pd.DataFrame(index=[pd.to_datetime(now.strftime(f'%Y-12-01'), utc=True)], data=[[entity, 0]],
                                    columns=['entity_id', 'value']), sort=True)
    df = df.sort_index()
    return df
