import sqlite3
from configparser import ConfigParser
from pathlib import Path
from tkinter.filedialog import asksaveasfilename

from model.config import CONFIG_FILE



def check_config_dbfile() -> bool:
    '''Prueft ob die Konfigurationsdatei die erforderlichen
    Sektionen usw. hat. Es wird dann ein Dialog zur Auswahl
    der Datenbank angezeigt. Wird eine Datenbankdatei ausgewählt,
    werden die erforderlichen Tabellen angelegt und die Funktion
    gibt *True* zurueck. Andernfalls wird 'False* zurueckgegeben'''

    cp = ConfigParser()
    cp.read(Path(CONFIG_FILE).expanduser())

    if not 'datenbank' in cp:
        cp.add_section('datenbank')

    with open(Path(CONFIG_FILE).expanduser(), mode='w') as cf:
        cp.write(cf)
        cf.close()

    if 'dbfile' in cp['datenbank']:
        return True

    filename = asksaveasfilename(defaultextension='Sqlite Datenbank (*.db)', filetypes=[(
        'Sqlite Datenbank', '*.db'), ('Sqlite Datenbank', '*.sqlite')], confirmoverwrite=False)

    if not filename:
        return False

    cp['datenbank']['dbfile'] = filename
    with open(Path(CONFIG_FILE).expanduser(), mode='w') as cf:
        cp.write(cf)
        cf.close()

    return True


def create_tables() -> None:
    '''Legt die Datenbanktabellen an.'''

    statements = [
        """
CREATE TABLE IF NOT EXISTS person_t
(
	id INTEGER NOT NULL,
	typ TEXT NOT NULL,
	anrede TEXT,
	titel TEXT,
	nachname TEXT NOT NULL,
	vorname TEXT,
	geboren DATE,
	verstorben DATE,
	gekuendigt DATE,
	post_erg TEXT,
	strasse TEXT,
	plz TEXT,
	ort TEXT,
	land TEXT,
	tel1 TEXT,
	tel2 TEXT,
	email TEXT,
	kdnr TEXT,
	hinweise TEXT,
	valid CHAR(1) NOT NULL DEFAULT('1'),
	von datetime NOT NULL DEFAULT(datetime('now')),
	bis datetime NOT NULL DEFAULT(datetime('9999-12-31T23:59:59')),
	
	UNIQUE (id, bis)
)""", """
CREATE INDEX IF NOT EXISTS idx_person_nachname ON person_t(nachname)
""", """
CREATE TABLE IF NOT EXISTS verbund_t
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	typ TEXT NOT NULL,

	von datetime NOT NULL DEFAULT(datetime('now')),
	bis datetime NOT NULL DEFAULT(datetime('9999-12-31T23:59:59')),
	
	UNIQUE (id, bis)
)
""", """
CREATE TABLE IF NOT EXISTS verbund_mitglieder_t
(
	verb_id INTEGER NOT NULL,
	pers_id INTEGER NOT NULL,
	rolle TEXT NOT NULL,
	hinweis TEXT,
	von datetime NOT NULL DEFAULT(datetime('now')),
	bis datetime NOT NULL DEFAULT(datetime('9999-12-31T23:59:59'))
)
""", """
CREATE TABLE IF NOT EXISTS konten_t
(
	id INTEGER NOT NULL,
	inh_id INTEGER,
	prod_var TEXT,
	gekuendigt DATE,
	valid CHAR(1) NOT NULL DEFAULT('1'),
	von datetime NOT NULL DEFAULT(datetime('now')),
	bis datetime NOT NULL DEFAULT(datetime('9999-12-31T23:59:59')),
	
	UNIQUE (id, bis)
)
""", """
CREATE TABLE IF NOT EXISTS buch_kopf_t
(
	id INTEGER NOT NULL UNIQUE,
	von datetime NOT NULL DEFAULT(datetime('now')),
	buchtag date NOT NULL DEFAULT(date('now')),
	valuta date NOT NULL DEFAULT(date('now')),
	buchtext TEXT
)
""", """
CREATE TABLE IF NOT EXISTS buch_daten_t
(
	buch_id INTEGER NOT NULL,
	kto INTEGER NOT NULL,
	schluessel INTEGER NOT NULL DEFAULT(0),
	betrag NUMERIC(18,2) NOT NULL
)
""", """
CREATE VIEW IF NOT EXISTS kontoumsaetze_v AS

SELECT
	bd.kto,
	bk.von,
	bk.buchtag,
	bk.valuta,
	bk.buchtext,
	bd.schluessel,
	bd.betrag,
	bd.buch_id
	
FROM	buch_kopf_t bk

JOIN	buch_daten_t bd
ON	bk.id = bd.buch_id

ORDER BY von
"""
    ]

    cp = ConfigParser()
    cp.read(Path(CONFIG_FILE).expanduser())

    dbfilename = cp['datenbank']['dbfile']
    db = sqlite3.connect(dbfilename)

    with db:
        cur = db.cursor()
        for sql in statements:
            cur.execute(sql)
        cur.close()


def set_highdpi():
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
