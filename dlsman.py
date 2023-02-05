import locale
import os
from configparser import ConfigParser
from pathlib import Path
from tkinter.messagebox import askokcancel, showinfo
from ttkbootstrap.localization import MessageCatalog

import model.config
from model.controller import Controller
from model.sql_db_manager import SqliteManager
from view.mainwin import MainWindow


def set_lang():
    '''Setzt die Sprache'''
    if not "LANG" in os.environ:
        os.environ['LANG'] = 'de_DE.UTF-8'

    locale.setlocale(locale.LC_ALL, os.environ['LANG'])


def checksetup():
    from view.setup import check_config_dbfile, create_tables, set_highdpi
    set_highdpi()

    if not check_config_dbfile():
        askokcancel("Abbruch: Keine gueltige Datenbank ausgewählt",
                    "Es wurde kein gültiger Datenbankname ausgewählt und in der Konfigurationsdatei gespeichert.")
        exit(1)

    create_tables()


def get_database_path() -> Path:
    cfg = ConfigParser()
    pfad = Path(model.config.CONFIG_FILE).expanduser()
    cfg.read(pfad)
    return cfg['datenbank']['dbfile']


def main():
    checksetup()
    set_lang()

    controller = Controller()
    sm = SqliteManager(get_database_path())

    controller.person_manager = sm
    controller.verbund_manager = sm
    controller.konten_manager = sm
    app = MainWindow(controller)
    controller.nachricht_anzeigen(f"Datenbank: {get_database_path()}")

    app.mainloop()
    sm.close()


if __name__ == '__main__':
    main()
