import json
import traceback
from datetime import datetime
from time import sleep

import pytz
from influxdb import DataFrameClient

from plot_electricity import make_electricity_plots
from plot_gas import make_gas_plots
from utils import NoInfluxDataError, get_min_max_datetimes_from_db

with open('./data/options.json', 'r') as f:
    settings = json.load(f)
settings['predicted solar'] = json.loads(settings['predicted solar'])

# Pandas DataFrame query results
client = DataFrameClient(host=settings['host'], port=settings['port'],
                         username=settings['username'], password=settings['password'])

print('Making historical electricity and gas plots...')
min_datetime = datetime.now(pytz.utc)
max_datetime = datetime.now(pytz.utc)

if settings['daily electricity usage db entity'] is not None:
    min_datetime, max_datetime = \
        get_min_max_datetimes_from_db(client, settings['daily electricity usage db entity'],
                                      settings['db_unit_prefix'], settings['db_unit_suffix'], 'kWh',
                                      min_datetime, max_datetime)
if settings['daily yield db entity'] is not None:
    min_datetime, max_datetime = \
        get_min_max_datetimes_from_db(client, settings['daily yield db entity'],
                                      settings['db_unit_prefix'], settings['db_unit_suffix'], 'kWh',
                                      min_datetime, max_datetime)

for year in range(min_datetime.year, max_datetime.year + 1):
    for month in range(1, 13):
        now = datetime(year, month, 1)
        print(f'Processing {now.year}-{now.month}')
        try:
            make_electricity_plots(settings, client, now)
            make_gas_plots(settings, client, now)
        except NoInfluxDataError as e:
            pass

while True:
    try:
        now = datetime.now()

        print('Making current electricity plots...')
        make_electricity_plots(settings, client, now)

        print('Making current gas plots...')
        make_gas_plots(settings, client, now)

    except NoInfluxDataError as e:
        print(f'The database returned an empty DataFrame, this might be because it is the first of the month right '
              f'after midnight, so there is no data yet. Continuing...')
    except Exception as e:
        print(f'The following error has occurred: {e}')
        print(f'Traceback:\n{traceback.format_exc()}')
        raise

    print(f"Sleeping for {settings['refresh time']}s")
    sleep(settings['refresh time'])
