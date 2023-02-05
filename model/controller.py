from datetime import date, datetime
from typing import Callable, Sequence

from model.db_manager import (BuchSatz, KontenManager, PersonManager)
from model.konto import Konto
from model.person import Person
from model.umsatz import Umsatz


class Controller():

    EVT_PERSONEN_SUCHEN = 1
    EVT_PERSONENDETAILS_ANZEIGEN = 2
    EVT_PERSONENLISTE_ANZEIGEN = 3
    EVT_PERSON_AENDERN = 4
    EVT_NACHRICHT = 5
    EVT_KONTOUEBERSICHT_ANZEIGEN = 6
    EVT_KONTO_ANLEGEN_ANZEIGEN = 7
    EVT_BUCHUNGSMASKE_ANZEIGEN = 8
    EVT_KONTO_AENDERN_ANZEIGEN = 9
    EVT_KONTO_AENDERN = 10
    EVT_ANSCHRIFT_AUFBEREITEN_ANZEIGEN = 11

    def __init__(self) -> None:

        self.__listeners = {}

        self.person_manager: PersonManager = None
        self.verbund_manager = VerbundManager = None
        self.konten_manager: KontenManager = None

    def register(self, evt: int, f: Callable) -> None:
        '''Registriert einen Event Listener'''

        if not evt in self.__listeners:
            self.__listeners[evt] = set()

        self.__listeners[evt].add(f)

    def _getListener(self, evt: int) -> Callable:
        if evt in self.__listeners:
            return self.__listeners[evt]
        else:
            return set()

    def personen_suchen(self, suchbegriff: str) -> None:
        '''Startet die Personensuche'''

        result = self.person_manager.personen_suchen(suchbegriff)

        for f in self._getListener(self.EVT_PERSONEN_SUCHEN):
            f(result)

    def personenliste_anzeigen(self) -> None:
        '''Blendet die Personenliste ein'''

        if not self.EVT_PERSONENLISTE_ANZEIGEN in self.__listeners:
            return

        for f in self._getListener(self.EVT_PERSONENLISTE_ANZEIGEN):
            f()

    def personendetails_anzeigen(self, person_id: int) -> None:
        '''Die Personendaten zur gegebenen ID werden ermittelt'''

        person: Person = self.person_manager.person_lesen(person_id)
        kontenliste: Sequence[Konto] = self.konten_manager.konten_zu_person_lesen(
            person_id)

        for f in self._getListener(self.EVT_PERSONENDETAILS_ANZEIGEN):
            f(person, kontenliste)

    def person_aendern_bildschirm_anzeigen(self, person_id: int = None) -> None:
        '''Die Personendaten zur gegebenen ID werden ermittelt'''

        person: Person = None
        if person_id:
            person = self.person_manager.person_lesen(person_id)

        for f in self._getListener(self.EVT_PERSON_AENDERN):
            f(person)

    def person_aendern(self, person: Person) -> None:
        '''Speichert die Personendaten'''

        try:
            p_vorhanden: Person = None
            if person.id:
                p_vorhanden = self.person_manager.person_lesen(person.id)
            else:
                raise ValueError(f"Die uebergebene Person ist unbekannt")

            p_neu: Person = None
            if person != p_vorhanden:
                p_neu = self.person_manager.person_aendern(person)
                for f in self.__listeners[self.EVT_NACHRICHT]:
                    f(f"Personendaten wurden gespeichert")
            else:
                p_neu = p_vorhanden
                for f in self.__listeners[self.EVT_NACHRICHT]:
                    f(f"Neue Personendaten sind unverändert - keine Speicherung erfolgt")

            kontenliste: Sequence[Konto] = self.konten_manager.konten_zu_person_lesen(
                p_neu.id)

            for f in self._getListener(self.EVT_PERSONENDETAILS_ANZEIGEN):
                f(p_neu, kontenliste)
        except ValueError as ve:
            if not self.EVT_NACHRICHT in self.__listeners:
                print(f"Fehler bei der Personenänderung: '{ve.args}'")

            for f in self._getListener(self.EVT_NACHRICHT):
                f(ve.args)

    def person_anlegen(self, person: Person) -> None:
        '''Legt die Person neu an'''

        try:
            p_neu: Person = None
            p_neu = self.person_manager.person_anlegen(person)
            for f in self.__listeners[self.EVT_NACHRICHT]:
                f(f"Personendaten wurden gespeichert")

            kontenliste: Sequence[Konto] = self.konten_manager.konten_zu_person_lesen(
                p_neu.id)

            for f in self._getListener(self.EVT_PERSONENDETAILS_ANZEIGEN):
                f(p_neu, kontenliste)

        except ValueError as ve:
            if not self.EVT_NACHRICHT in self.__listeners:
                print(f"Fehler bei der Personenänderung: '{ve.args}'")

            for f in self._getListener(self.EVT_NACHRICHT):
                f(ve.args)

    def kontouebersicht_anzeigen(self, konto_id: int) -> None:
        '''Ruft die Kontoübersicht zum angegebenen Konto auf'''

        kto: Konto = self.konten_manager.konto_lesen(konto_id)
        umsaetze: Sequence[Umsatz] = self.konten_manager.buchungen_lesen(
            konto_id)

        for f in self._getListener(self.EVT_KONTOUEBERSICHT_ANZEIGEN):
            f(kto, umsaetze)

    def buchungsmaske_anzeigen(self) -> None:
        '''Ruft die Buchungsmaske auf'''

    def nachricht_anzeigen(self, message: str) -> None:
        '''Loggt eine Nachricht'''

        for f in self._getListener(self.EVT_NACHRICHT):
            f(message)

    def konto_anlegen_anzeigen(self, person_id: int) -> None:
        '''Ruft den Bildschirm zur Kontoanlage auf'''

        konten = self.konten_manager.konten_zu_person_lesen(person_id)
        person = self.person_manager.person_lesen(person_id)

        hat_mitgliedskonto = False
        hat_kundenkonto = False
        for k in konten:
            if k.prod_var == 'Mitgliedskonto':
                hat_mitgliedskonto = True
            elif k.prod_var == 'Einkaufskonto':
                hat_kundenkonto = True

        produktauswahl = []
        if not hat_kundenkonto:
            produktauswahl.append('Einkaufskonto')
        if not hat_mitgliedskonto:
            produktauswahl.append('Mitgliedskonto')

        for f in self._getListener(self.EVT_KONTO_ANLEGEN_ANZEIGEN):
            f(person, produktauswahl)

    def konto_anlegen(self, person_id: int, prodvar: str) -> None:
        '''Führt die Kontoanlage durch'''
        person = self.person_manager.person_lesen(person_id)
        if not person:
            self.nachricht_anzeigen(
                f"Es ist keine Person mit der ID '{person_id}' bekannt")

        konto = self.konten_manager.konto_anlegen(person_id, prodvar)

        self.personendetails_anzeigen(person_id)

    def buchungsmaske_anzeigen(self) -> None:
        '''Zeigt die Buchungsmaske an'''

        for f in self._getListener(self.EVT_BUCHUNGSMASKE_ANZEIGEN):
            f()

    def pruefe_konten(self, ktn: Sequence[BuchSatz]) -> Sequence[str]:
        '''Prüft die Konten auf Vorhandensein und liefert die Namen zurueck'''

        result = []

        for satz in ktn:
            if satz.kto == 0:
                result.append('')
            else:
                konto = self.konten_manager.konto_lesen(satz.kto)
                if konto:
                    result.append(konto.inh_name)
                else:
                    result.append('Konto existiert nicht')

        return result

    def buchen(self, buchtext: str, ktn_betraege: Sequence[BuchSatz], valuta: date) -> None:
        '''Führt die Buchung aus'''
        try:
            self.konten_manager.buchen(buchtext, ktn_betraege, valuta)
            self.nachricht_anzeigen(f"Buchung wurde ausgeführt")
            self.buchungsmaske_anzeigen()
        except ValueError as ve:
            self.nachricht_anzeigen(f"Fehler beim Buchen: {ve.args}")

    def konto_aendern_anzeigen(self, kto_id: int) -> None:
        '''Zeigt den Konto-Ändern-Bildschirm'''

        konto = self.konten_manager.konto_lesen(kto_id)

        for f in self._getListener(self.EVT_KONTO_AENDERN_ANZEIGEN):
            f(konto)

    def konto_aendern(self, kto_id: str, gekuendigt: str) -> None:
        '''Ruft die Kündigung auf'''

        konto = self.konten_manager.konto_lesen(int(kto_id))
        if not konto:
            raise ValueError(f"Das Konto mit der ID '' ist nicht bekannt")

        kd_datum = datetime.strptime(gekuendigt, '%d.%m.%Y').date()
        self.konten_manager.konto_kuendigen(int(kto_id), kd_datum)
        self.nachricht_anzeigen(f"Konto mit der ID '{kto_id}' wurde geändert")
        self.kontouebersicht_anzeigen(int(kto_id))

    def anschrift_aufbereiten_anzeigen(self, person_id: int) -> None:
        '''Ruft den Bildschirm zur Aufbereitung der Anschrift auf'''

        person = self.person_manager.person_lesen(person_id)
        
        for f in self._getListener(self.EVT_ANSCHRIFT_AUFBEREITEN_ANZEIGEN):
            f(person)