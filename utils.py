from dateutil.parser import parse as dparse, ParserError
import logging

log = logging.getLogger(__name__)


def configure_loggers():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)s %(levelname)s '
                        '%(filename)s:%(lineno)s  %(message)s')
    list_loggers = list(logging.root.manager.loggerDict.keys()) + [
        'RobotFramework',
        'openai',
    ]

    for log_name in list_loggers:
        if 'spiders' in log_name:
            continue
        logging.getLogger(log_name).setLevel(logging.CRITICAL)


def get_date_from_string(date_str):
    if date_str == '':
        return ''

    def _retry_date(date_txt):
        list_elements = date_txt.split(' ')
        for i in range(len(list_elements)):
            d = ' '.join(list_elements[i:i + 3])
            try:
                return dparse(d, fuzzy=True)
            except ParserError:
                continue
        return date_txt

    try:
        return dparse(date_str, fuzzy=True).date()
    except ParserError:
        log.error(f'date_str {date_str} not parse')
        return _retry_date(date_str)


def send_heartbeat():
    log.info('send notify of success')
