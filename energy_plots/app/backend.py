import json
import traceback
from datetime import datetime
from time import sleep

import pytz
from influxdb import DataFrameClient

from app import app
from app.plot_electricity import make_electricity_plots
from app.plot_gas import make_gas_plots
from app.utils import NoInfluxDataError, get_min_max_datetimes_from_db


def main_thread():
    app.logger.info('Entering main thread...')

    app.logger.info('Loading config')
    with open('./data/options.json', 'r') as f:
        settings = json.load(f)
    if settings.get('predicted solar'):
        settings['predicted solar'] = json.loads(settings['predicted solar'])

    # Pandas DataFrame query results
    app.logger.info('Setting up database client')
    client = DataFrameClient(host=settings['host'], port=settings['port'],
                             username=settings['username'], password=settings['password'])

    app.logger.info('Querying min/max datetime from database')
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

    app.logger.info('Making historical electricity and gas plots')
    for year in range(min_datetime.year, max_datetime.year + 1):
        for month in range(1, 13):
            now = datetime(year, month, 1)
            app.logger.info(f'Processing {now.year}-{now.month}')
            try:
                make_electricity_plots(settings, client, now)
                make_gas_plots(settings, client, now)
            except NoInfluxDataError as e:
                pass
    app.logger.info('Done with historical plots')

    while True:
        try:
            now = datetime.now()

            app.logger.info('Making current electricity plots')
            make_electricity_plots(settings, client, now)

            app.logger.info('Making current gas plots')
            make_gas_plots(settings, client, now)

        except NoInfluxDataError as e:
            app.logger.info(f'The database returned an empty DataFrame, this might be because it is the first of the '
                            f'month right after midnight, so there is no data yet. Continuing...')
        except Exception as e:
            app.logger.info(f'The following error has occurred: {e}')
            app.logger.info(f'Traceback:\n{traceback.format_exc()}')
            raise

        app.logger.info('Done with current plots')
        app.logger.info(f"Sleeping for {settings['refresh time']}s")
        sleep(settings['refresh time'])
