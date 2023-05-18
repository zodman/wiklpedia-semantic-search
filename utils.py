from dateutil.parser import parse as dparse
from dotenv import load_dotenv, find_dotenv
import logging
load_dotenv(find_dotenv())

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


for log_name in list(logging.root.manager.loggerDict.keys()) + [
        'RobotFramework',
]:
    logging.getLogger(log_name).setLevel(logging.CRITICAL)


def get_date_from_string(date_str):
    try:
        return dparse(date_str, fuzzy=True).date()
    except dparse.ParserError:
        log.error(f'date_str {date_str} not parse')
        return None
