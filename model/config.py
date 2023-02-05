from os.path import dirname, join
from pathlib import Path

ROOT_DIR = dirname(dirname(__file__))
RES_DIR = join(ROOT_DIR, 'res')


APP_NAME = 'DLS Manager'
APP_ID = 'dlsman'
APP_ORGANISATION = 'Unser Dorfladen Schlichten eG'
APP_DOMAIN = 'dorfladen-schlichten.de'

CONFIG_FILE = "~/.dlsman.ini"


def ensure_config_file():
    '''Stellt sicher, dass die Konfigurationsdatei angelegt ist'''
    config_path = Path(CONFIG_FILE).expanduser().absolute()
    config_path.touch(exist_ok=True)


ensure_config_file()
