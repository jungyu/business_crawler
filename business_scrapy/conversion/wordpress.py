import sys
import re
import loguru
import json

import sqlalchemy
import sqlalchemy.ext.automap

from ..database.connection import session, metadata, automap

class Wordpress():

    def __init__(self):
        loguru.logger.info('init')

    def main(self):
        loguru.logger.info('main')

    def start_parse(self):
        loguru.logger.info('start_parse')
    
