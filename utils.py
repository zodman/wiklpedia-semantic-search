from dateutil.parser import parse as dparse, ParserError
from dotenv import load_dotenv, find_dotenv
import os
import logging

load_dotenv(find_dotenv())

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

list_loggers = list(logging.root.manager.loggerDict.keys()) + [
    'RobotFramework',
]

for log_name in list_loggers:
    logging.getLogger(log_name).setLevel(logging.CRITICAL)

SCIENTISTS = [
    "Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin"
]
HEADLESS = os.environ.get("HEADLESS")

DATE_FORMAT = "%-d %B %Y"


def get_date_from_string(date_str):

    try:
        return dparse(date_str, fuzzy=True).date()
    except ParserError:
        log.error(f'date_str {date_str} not parse')
        return date_str
