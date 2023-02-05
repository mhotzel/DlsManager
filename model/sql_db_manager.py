import sqlite3
from datetime import date
from typing import List, Sequence

from model.db_manager import BuchSatz
from model.konto import Konto
from model.person import Person
from model.umsatz import Umsatz
from model.verbund import Verbund


def _row_as_person(row) -> Person:
    p = Person(
        id=int(row[0]),
        typ=row[1],
        anrede=row[2],
        titel=row[3],
        nachname=row[4],
        vorname=row[5],
        geboren=date.fromisoformat(row[6]) if row[6] else None,
        verstorben=date.fromisoformat(row[7]) if row[7] else None,
        gekuendigt=date.fromisoformat(row[8]) if row[8] else None,
        post_erg=row[9],
        strasse=row[10],
        plz=row[11],
        ort=row[12],
        land=row[13],
        tel1=row[14],
        tel2=row[15],
        email=row[16],
        kdnr=row[17],
        hinweise=row[18]
    )
    return p


def _person_as_tuple(p: Person) -> tuple:
    return (p.id, p.typ, p.anrede, p.titel, p.nachname, p.vorname, p.geboren, p.verstorben, p.gekuendigt, p.post_erg, p.strasse, p.plz, p.ort, p.land, p.tel1, p.tel2, p.email, p.kdnr, p.hinweise)


def _row_as_konto(row) -> Konto:
    k = Konto(
        id=int(row[0]),
        inh_id=int(row[1]),
        inh_name=row[2],
        prod_var=row[3],
        gekuendigt=date.fromisoformat(row[4]) if row[4] else None,
        saldo=row[5]
    )
    return k


def _row_as_umsatz(row) -> Umsatz:
    u = Umsatz(
        kto=row[0],
        von=row[1],
        buchtag=date.fromisoformat(row[2]) if row[2] else None,
        valuta=date.fromisoformat(row[3]) if row[3] else None,
        buchtext=row[4],
        schluessel=row[5],
        betrag=row[6],
        buch_id=row[7]
    )
    return u


class SqliteManager():
    '''Verwaltet Personen in einer SQLITE-Datenbank'''

    def __init__(self, dbfile: str) -> None:
        self._db = sqlite3.connect(dbfile)

    def close(self):
        '''Schliesst die Datenbank und gibt die Ressourcen frei'''
        self._db.close()

    def person_lesen(self, id: int) -> Person:
        '''liest eine Person anhand ihrer eindeutigen ID.'''
        with self._db:
            return self._person_lesen(self._db, id)

    def _person_lesen(self, conn: sqlite3.Connection, id: int) -> Person:

        SQL = """
        SELECT p.id, p.typ, p.anrede, p.titel, p.nachname, p.vorname, p.geboren, p.verstorben, p.gekuendigt, p.post_erg, p.strasse, p.plz, p.ort, p.land, p.tel1, p.tel2, p.email, p.kdnr, p.hinweise
        FROM person_t AS p
        WHERE   p.valid = '1'
            AND p.id = ?
        """

        result: Person = None

        cur = conn.cursor()

        row = cur.execute(SQL, (id,)).fetchone()
        result = None
        if row:
            result = _row_as_person(row)
        cur.close()

        return result

    def personen_lesen(self, offset: int = 0, count: int = 10) -> Sequence[Person]:
        '''liest eine Anzahl von Personen, beginnend beim angegebenen Offset.'''
        with self._db:
            return self._personen_lesen(self._db, offset, count)

    def _personen_lesen(self, conn: sqlite3.Connection, offset: int, count: int) -> Sequence[Person]:

        SQL = """
        SELECT p.id, p.typ, p.anrede, p.titel, p.nachname, p.vorname, p.geboren, p.verstorben, p.gekuendigt, p.post_erg, p.strasse, p.plz, p.ort, p.land, p.tel1, p.tel2, p.email, p.kdnr, p.hinweise
        FROM person_t AS p
        WHERE   p.valid = '1'
        ORDER BY p.id
        LIMIT ?
        OFFSET ?
        """

        result: List[Person] = []
        cur = conn.cursor()
        res = cur.execute(SQL, (count, offset)).fetchall()
        for r in res:
            result.append(_row_as_person(r))
        cur.close()

        return result

    def personen_suchen(self, name: str) -> Sequence[Person]:
        '''ermittelt alle Personen, deren Namen den uebergebenen Namen enthaelt.'''
        with self._db:
            return self._personen_suchen(self._db, name)

    def _personen_suchen(self, conn: sqlite3.Connection, name: str) -> Sequence[Person]:

        SQL = """
        SELECT p.id, p.typ, p.anrede, p.titel, p.nachname, p.vorname, p.geboren, p.verstorben, p.gekuendigt, p.post_erg, p.strasse, p.plz, p.ort, p.land, p.tel1, p.tel2, p.email, p.kdnr, p.hinweise
        FROM person_t AS p
        WHERE   p.valid = '1'
            AND p.nachname LIKE ?
        ORDER BY p.id
        """

        result: List[Person] = []

        cur = conn.cursor()
        res = cur.execute(SQL, (f"%{name}%",)).fetchall()
        for r in res:
            result.append(_row_as_person(r))
        cur.close()

        return result

    def person_anlegen(self, person: Person) -> Person:
        '''Legt eine Person an und gibt die erzeugte ID zurueck, falls keine ID mitgegeben wurde.'''

        with self._db:
            id = self._person_anlegen(self._db, person)
            person_result = self._person_lesen(self._db, id)
            return person_result

    def _person_anlegen(self, conn: sqlite3.Connection, person: Person) -> int:

        if person.typ not in ('P', 'G', 'J'):
            raise ValueError(
                f"Personentyp muss einer der Werte ('P', 'G', 'J') sein, ist jedoch '{person.typ}'")

        if not person.nachname:
            raise ValueError(f"Der Nachname ist ein Pflichtfeld")

        SQL_MAX_ID = '''
        SELECT COALESCE(MAX(p.id), 0) AS max_id
        FROM person_t AS p
        '''

        SQL_ANLEGEN = '''
        INSERT INTO person_t (id, typ, anrede, titel, nachname, vorname, geboren, verstorben, gekuendigt, post_erg, strasse, plz, ort, land, tel1, tel2, email, kdnr, hinweise)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''

        id: int = None

        cur = conn.cursor()
        if not person.id:
            id = cur.execute(SQL_MAX_ID).fetchone()[0] + 1
            person.id = id

        cur.execute(SQL_ANLEGEN, _person_as_tuple(person))
        cur.close()

        return id if id else person.id

    def person_aendern(self, person: Person) -> Person:
        '''aendert die Personendaten zur Person mit der uebergebenen ID und gibt die aktualisierte Person zurueck.'''

        with self._db:
            if not person.id:
                raise ValueError(f"Person enthaelt keine ID")

            if person.typ not in ('P', 'G', 'J'):
                raise ValueError(
                    f"Personentyp muss einer der Werte ('P', 'G', 'J') sein, ist jedoch '{person.typ}'")

            if not person.nachname:
                raise ValueError(f"Der Nachname ist ein Pflichtfeld")

            p_vorhanden = self._person_lesen(self._db, person.id)
            if not p_vorhanden:
                raise LookupError(
                    f"Es ist keine Person mit der ID '{person.id}' vorhanden.")

            if p_vorhanden == person:
                return person

            self._person_aendern(self._db, person)
            return self._person_lesen(self._db, person.id)

    def _person_aendern(self, conn: sqlite3.Connection, person: Person) -> None:

        SQL_BIS = '''
        UPDATE person_t SET bis = datetime('now'), valid='0' WHERE id = ? AND bis >= datetime('now')
        '''

        SQL_ANLEGEN = '''
        INSERT INTO person_t (id, typ, anrede, titel, nachname, vorname, geboren, verstorben, gekuendigt, post_erg, strasse, plz, ort, land, tel1, tel2, email, kdnr, hinweise)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''

        cur = conn.cursor()
        cur.execute(SQL_BIS, (person.id, ))
        cur.execute(SQL_ANLEGEN, _person_as_tuple(person))
        cur.close()

    def person_loeschen(self, id: int) -> None:
        '''Loescht die angegebene Person. Die Loeschung erfolgt nur logisch durch Setzen des BIS-Datums.'''
        with self._db:
            person = self._person_lesen(self._db, id)
            if not person:
                raise ValueError(
                    f"Es ist keine Person mit der ID '{id}' vorhanden")

            return self._person_loeschen(self._db, id)

    def _person_loeschen(self, conn: sqlite3.Connection, id: int) -> None:

        SQL = '''
        UPDATE person_t SET bis = datetime('now'), valid='0' WHERE id = ? AND bis >= datetime('now')
        '''

        cur = conn.cursor()
        cur.execute(SQL, (id, ))
        cur.close()

    def verbund_lesen(self, id: int) -> Verbund:
        '''Ermittelt den Verbund zur angegebenen ID.'''

        with self._db:
            return self._verbund_lesen(self._db, id)

    def _verbund_lesen(self, conn: sqlite3.Connection, id: int) -> Verbund:

        SQL_LESEN = '''
        SELECT v.id, v.typ FROM verbund_t AS v
        WHERE   v.von <= datetime('now')
	        AND v.bis > datetime('now')
            AND v.id = ?
        '''

        verb: Verbund = None

        cur = conn.cursor()
        row = cur.execute(SQL_LESEN, (id, )).fetchone()
        if not row:
            raise ValueError(
                f"Verbund mit der ID '{id}' ist nicht vorhanden")
        id = row[0]
        typ = row[1]
        verb = Verbund(id, typ)
        cur.close()

        return verb

    def verbund_anlegen(self, verb: Verbund) -> int:
        '''legt einen neuen leeren Verbund an und gibt die ID des neuen Verbundes zurueck'''

        with self._db:
            return self._verbund_anlegen(self._db, verb)

    def _verbund_anlegen(self, conn: sqlite3.Connection, verb: Verbund) -> int:

        if verb.typ not in Verbund.VERBUNDTYPEN:
            raise ValueError(f"Verbundtyp '{verb.typ}' ist nicht zulaessig")

        SQL_MAX_ID = '''
        SELECT COALESCE(MAX(v.id), 0) AS max_id
        FROM verbund_t AS v
        '''

        SQL_ANLEGEN = '''
        INSERT INTO verbund_t (id, typ) VALUES (?, ?)
        '''

        verb_id: int = None

        cur = conn.cursor()
        verb_id = cur.execute(SQL_MAX_ID).fetchone()[0] + 1
        verb.id = verb_id
        cur.execute(SQL_ANLEGEN, (verb.id, verb.typ))
        cur.close()

        return verb_id

    def verbund_loeschen(self, id: int) -> None:
        '''loescht den Verbund logisch'''

        with self._db:
            return self._verbund_loeschen(self._db, id)

    def _verbund_loeschen(self, conn: sqlite3.Connection, id: int) -> None:

        self.verbund_lesen(id)

        SQL_LOESCHEN = '''
        UPDATE verbund_t SET bis = datetime('now') WHERE id = ?'''

        cur = conn.cursor()
        cur.execute(SQL_LOESCHEN, (id, ))
        cur.close()

    def verbund_mitglied_hinzu(self, verbund_id: int, person_id: int, rolle: str) -> None:
        '''fuegt die Person zur angegebenen ID dem Verbund hinzu.'''

        with self._db:
            person = self._person_lesen(self._db, person_id)
            if not person:
                raise ValueError(
                    f"Es ist keine Person mit der ID '{person_id}' vorhanden.")

            verb = self._verbund_lesen(self._db, verbund_id)
            if not verb:
                raise ValueError(
                    f"Es ist kein Verbund mit der ID '{verbund_id}' vorhanden.")

            return self._verbund_mitglied_hinzu(self._db, verbund_id, person_id)

    def _verbund_mitglied_hinzu(self, conn: sqlite3.Connection, verbund_id: int, person_id: int, rolle: str) -> None:

        self.verbund_lesen(verbund_id)
        if rolle not in Verbund.VERBUNDROLLEN:
            raise ValueError(f"Verbundrolle '{rolle}' ist nicht zulaessig")

        SQL_EINFUEGEN = '''
        INSERT INTO verbund_mitglieder_t (verb_id, pers_id, rolle)
        VALUES (?, ?, ?)
        '''

        cur = conn.cursor()
        cur.execute(SQL_EINFUEGEN, (verbund_id, person_id, rolle))
        cur.close()

    def verbund_mitglied_entfernen(self, verbund_id: int, person_id: int, rolle: str = None) -> None:
        '''entfernt die Person zur angegebenen ID aus dem Verbund.'''

        with self._db:
            person = self._person_lesen(self._db, person_id)
            if not person:
                raise ValueError(
                    f"Es ist keine Person mit der ID '{person_id}' vorhanden.")

            verb = self._verbund_lesen(self._db, verbund_id)
            if not verb:
                raise ValueError(
                    f"Es ist kein Verbund mit der ID '{verbund_id}' vorhanden.")

            return self._verbund_mitglied_entfernen(self._db, verbund_id, person_id, rolle)

    def _verbund_mitglied_entfernen(self, conn: sqlite3.Connection, verbund_id: int, person_id: int, rolle: str) -> None:

        SQL_ENTFERNEN = """
        update verbund_mitglieder_t
        SET bis = datetime('now')
        WHERE   von <= datetime('now')
            AND bis > datetime('now')
            AND verb_id = ?
            AND pers_id = ?
        """

        if rolle:
            SQL_ENTFERNEN = SQL_ENTFERNEN + ' AND rolle = ?'

        cur = conn.cursor()

        if rolle:
            cur.execute(SQL_ENTFERNEN, (verbund_id, person_id, rolle))
        else:
            cur.execute(SQL_ENTFERNEN, (verbund_id, person_id))

        cur.close()

    def konto_lesen(self, konto_id: int) -> Konto:
        '''Liest die Kontodaten zum angegebenen Konto'''

        with self._db:
            return self._konto_lesen(self._db, konto_id)

    def _konto_lesen(self, conn: sqlite3.Connection, konto_id: int) -> Konto:

        SQL = """
        SELECT
            k.id,
            k.inh_id,
            CASE
                WHEN p.vorname IS NULL THEN p.nachname
                WHEN p.vorname = '' THEN p.nachname
                ELSE p.nachname || ', ' || p.vorname
            END AS inh_name,
            k.prod_var,
            k.gekuendigt,
            COALESCE(ums.saldo, 0) AS saldo
            
        FROM konten_t AS k
        LEFT JOIN (
            SELECT
                ums.kto,
                ROUND(SUM(ums.betrag), 2) AS saldo
            FROM kontoumsaetze_v ums
            GROUP BY ums.kto
        ) as ums
        ON 		k.id = ums.kto

        JOIN person_t AS p
        ON	k.inh_id = p.id
        AND p.valid = '1'

        WHERE 	k.valid = '1'
            AND k.id = ?
        """

        cur = conn.cursor()
        res = cur.execute(SQL, (konto_id, )).fetchone()
        kto: Konto = _row_as_konto(res) if res else None
        cur.close()
        return kto

    def konten_zu_person_lesen(self, person_id: int) -> Sequence[Konto]:
        '''Ermittelt alle Konten zu einer Person'''

        with self._db:
            person = self._person_lesen(self._db, person_id)
            if not person:
                raise ValueError(
                    f"Es ist keine Person mit der ID '{person_id}' bekannt.")
            return self._konten_zu_person_lesen(self._db, person_id)

    def _konten_zu_person_lesen(self, conn: sqlite3.Connection, person_id: int) -> Sequence[Konto]:

        SQL = """
        SELECT
            k.id,
            k.inh_id,
            CASE
                WHEN p.vorname IS NULL THEN p.nachname
                WHEN p.vorname = '' THEN p.nachname
                ELSE p.nachname || ', ' || p.vorname
            END AS inh_name,
            k.prod_var,
            k.gekuendigt,
            COALESCE(ums.saldo, 0) AS saldo
            
        FROM konten_t AS k
        LEFT JOIN (
            SELECT
                ums.kto,
                ROUND(SUM(ums.betrag), 2) AS saldo
            FROM kontoumsaetze_v ums
            GROUP BY ums.kto
        ) as ums
        ON 		k.id = ums.kto

        JOIN person_t AS p
        ON	k.inh_id = p.id
        AND p.valid = '1'

        WHERE 	k.valid = '1'
            AND p.id = ?
        """

        ktoliste: Sequence[Konto] = []

        cur = conn.cursor()
        res = cur.execute(SQL, (person_id, ))
        for row in res:
            ktoliste.append(_row_as_konto(row))

        cur.close()

        return ktoliste

    def konto_anlegen(self, person_id: int, prod_var: str) -> Konto:
        '''Legt ein neues Konto mit der gegebenen Produktvariante ::prod_var an.'''

        if not prod_var:
            raise (f"Die Produktvariante muss gefuellt sein")

        with self._db:
            person = self._person_lesen(self._db, person_id)
            if not person:
                raise ValueError(
                    f"Es ist keine Person mit der ID '{person_id}' bekannt.")

            ktn: Sequence[Konto] = self._konten_zu_person_lesen(
                self._db, person_id)

            if prod_var == 'Mitgliedskonto':
                mitgliedskonten = [
                    kto for kto in ktn if kto.prod_var == 'Mitgliedskonto']
                if len(mitgliedskonten) > 0:
                    raise ValueError(
                        f"Jede Person kann nur ein Mitgliedskonto haben")

            konto_id = self._konto_anlegen(self._db, person_id, prod_var)
            return self._konto_lesen(self._db, konto_id)

    def _konto_anlegen(self, conn: sqlite3.Connection, person_id: int, prod_var: str) -> int:

        SQL_MAX_ID = '''
        SELECT COALESCE(MAX(k.id), 0) AS max_id
        FROM konten_t AS k
        '''

        SQL = """
        INSERT INTO konten_t (id, inh_id, prod_var) VALUES(?, ?, ?)
        """

        cur = conn.cursor()
        max_id = cur.execute(SQL_MAX_ID).fetchone()[0] + 1
        cur.execute(SQL, (max_id, person_id, prod_var))
        cur.close()

        return max_id

    def konto_aendern(self, konto: Konto) -> Konto:
        '''Ändert das Konto. Gibt das geänderte Konto zurück.'''

        with self._db:
            kto_vorhanden = self._konto_lesen(konto.id)
            if not kto_vorhanden:
                raise ValueError(f"Es ist kein Konto mit der ID '' bekannt")

            if kto_vorhanden == konto:
                return konto

            return self._konto_lesen(self._db, konto.id)

    def _konto_aendern(self, conn: sqlite3.Connection, konto: Konto) -> None:
        '''Ändert das Konto.'''

        SQL_DELETE = """
        UPDATE konten_t SET valid = '0', bis = datetime('now')
        WHERE id = ? AND bis >= datetime('now')
        """

        SQL_INSERT = """
        INSERT INTO konten_t (id, inh_id, prod_var, gekuendigt) VALUES(?, ?, ?, ?)
        """

        cur = conn.cursor()
        cur.execute(SQL_DELETE, (konto.id, ))
        cur.execute(SQL_INSERT, (konto.id, konto.inh_id,
                    konto.prod_var, konto.gekuendigt))
        cur.close()

    def konto_kuendigen(self, kto_id: int, kdg_datum: date) -> Konto:
        '''Kündigt das Konto'''

        with self._db:
            kto: Konto = self._konto_lesen(self._db, kto_id)
            if not kto:
                raise ValueError(f"Es ist kein Konto mit der ID '' bekannt")

            if kto.gekuendigt == kdg_datum:
                return kto

            kto.gekuendigt = kdg_datum

            self._konto_aendern(self._db, kto)
            return self._konto_lesen(self._db, kto_id)

    def konto_loeschen(self, konto_id: int) -> None:
        '''Loescht bzw. historisiert das angegebene Konto.'''

        with self._db:
            kto = self._konto_lesen(self._db, konto_id)
            if not kto:
                raise ValueError(
                    f"Das Konto mit der ID '{konto_id}' ist nicht vorhanden")
            self._konto_loeschen(self._db, konto_id)

    def _konto_loeschen(self, conn: sqlite3.Connection, konto_id: int) -> None:

        SQL = """
        UPDATE konten_t SET valid = '0', bis = datetime('now')
        WHERE id = ? AND bis >= datetime('now')
        """

        cur = conn.cursor()
        cur.execute(SQL, (konto_id, ))
        cur.close()

    def buchen(self, buchtext: str, ktn_betraege: Sequence[BuchSatz], valuta: date = None) -> None:
        '''Fuehrt eine Buchung durch'''
        if not valuta:
            valuta = date.today()

        if len(buchtext) < 1:
            raise ValueError(f"Der Buchungstext darf nicht leer sein")

        if len(ktn_betraege) < 2:
            raise ValueError(
                f"Es muessen mindestens 2 Konten angesprochen werden")

        with self._db:
            betragssumme = 0.0
            for satz in ktn_betraege:
                kto_id = satz.kto
                betragssumme += satz.betrag
                if not self._konto_lesen(self._db, kto_id):
                    raise ValueError(
                        f"Das angegebene Konto mit der ID '{kto_id}' ist nicht vorhanden")

            if round(betragssumme, 2) != 0.0:
                raise ValueError(
                    f"Die Summe aller Soll- und Habenbuchungen ist nicht '0'")

            buch_id = self._schreibe_buchkopf(self._db, buchtext, valuta)
            self._schreibe_buchungen(self._db, buch_id, ktn_betraege)

    def _schreibe_buchkopf(self, conn: sqlite3.Connection, buchtext: str, valuta: date) -> int:
        '''Schreibt die Kopfdaten der Buchung'''

        SQL_MAX_ID = """
        SELECT COALESCE(MAX(b.id), 0) AS max_id
        FROM buch_kopf_t AS b 
        """

        SQL = """
        INSERT INTO buch_kopf_t (id, buchtext, valuta) VALUES (?, ?, ?);
        """

        cur = conn.cursor()
        buch_id = cur.execute(SQL_MAX_ID).fetchone()[0] + 1
        cur.execute(SQL, (buch_id, buchtext, valuta))
        cur.close()

        return buch_id

    def _schreibe_buchungen(self, conn: sqlite3.Connection, buch_id: int, ktn_betraege: Sequence[BuchSatz]) -> None:
        '''Schreibt die Buchung'''

        SQL = """
        INSERT INTO buch_daten_t (buch_id, kto, schluessel, betrag)
        VALUES (?, ?, ?, ?)
        """

        cur = conn.cursor()
        for satz in ktn_betraege:
            cur.execute(SQL, (buch_id, satz.kto, satz.schluessel, satz.betrag))
        cur.close()

    def buchungen_lesen(self, konto_id: int) -> Umsatz:
        '''Liest die Buchungen zum angegebenen Konto'''

        with self._db:
            kto = self._konto_lesen(self._db, konto_id)
            if not kto:
                raise ValueError(
                    f"Es ist kein Konto mit der ID '{konto_id}' vorhanden")

            return self._buchungen_lesen(self._db, konto_id)

    def _buchungen_lesen(self, conn: sqlite3.Connection, konto_id: int) -> Umsatz:

        SQL = """
        SELECT
            u.kto,
            u.von,
            u.buchtag,
            u.valuta,
            u.buchtext,
            u.schluessel,
            u.betrag,
            u.buch_id

        FROM kontoumsaetze_v AS u
        WHERE u.kto = ?
        ORDER BY u.von
        """

        umsaetze: Sequence[Umsatz] = []

        cur = self._db.cursor()
        result = cur.execute(SQL, (konto_id, )).fetchall()
        for umsatz in result:
            umsaetze.append(_row_as_umsatz(umsatz))
        cur.close()

        return umsaetze
