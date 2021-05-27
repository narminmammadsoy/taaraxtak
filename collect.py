# taaraxtak
# nick merrill
# 2021
#
# create-tables.py - defines the Postgres tables.
# this runs always.

import time
import schedule
import psycopg2
import logging
import coloredlogs
from funcy import partial

from src.w3techs.collect import collect as w3techs_collect
from src.ooni.collect import collect as ooni_collect

from config import config

#
# setup
#
logging.basicConfig()
logger = logging.getLogger("taaraxtak:collect")
# logger.setLevel(logging.DEBUG)
coloredlogs.install()
# coloredlogs.install(level='INFO')
coloredlogs.install(level='DEBUG')

# connect to the db
connection = psycopg2.connect(**config['postgres'])
cursor = connection.cursor()
logging.info('Connected to database.')

# configure scrapers for the db
w3techs = partial(w3techs_collect, cursor, connection)
ooni = partial(ooni_collect, cursor, connection)

#
# run
#

schedule.every().day.at('09:00').do(w3techs)
schedule.every(1).minutes.do(ooni)

while True:
    schedule.run_pending()
    time.sleep(1)
