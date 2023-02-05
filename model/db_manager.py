from datetime import date
from typing import NamedTuple, Protocol, Sequence

from model.konto import Konto
from model.person import Person
from model.umsatz import Umsatz
from model.verbund import Verbund


class BuchSatz(NamedTuple):
    kto: int
    schluessel: int
    betrag: float


class PersonManager(Protocol):
    '''Interface zum Management von Personen.'''

    def person_lesen(self, id: int) -> Person:
        '''liest eine Person anhand ihrer eindeutigen ID.'''
        ...

    def personen_lesen(self, offset: int = 0, count: int = 10) -> Sequence[Person]:
        '''liest eine Anzahl von Personen, beginnend beim angegebenen Offset.'''
        ...

    def personen_suchen(self, name: str) -> Sequence[Person]:
        '''ermittelt alle Personen, deren Namen den uebergebenen Namen enthaelt.'''
        ...

    def person_anlegen(self, member: Person) -> Person:
        '''Legt eine Person an und gibt die erzeugte ID zurueck, falls keine ID mitgegeben wurde.'''
        ...

    def person_aendern(self, member: Person) -> Person:
        '''aendert die Personendaten zur Person mit der uebergebenen ID und gibt die aktualisierte Person zurueck.'''
        ...

    def person_loeschen(self, id: int) -> None:
        '''Loescht die angegebene Person. Die Loeschung erfolgt nur logisch durch Setzen des BIS-Datums.'''


class VerbundManager(Protocol):
    '''Interface zur Verwaltung von Personenverbuenden'''

    def verbund_lesen(self, id: int) -> Verbund:
        '''Ermittelt den Verbund zur angegebenen ID.'''
        ...

    def verbund_anlegen(self, verb: Verbund) -> int:
        '''legt einen neuen leeren Verbund an und gibt die ID des neuen Verbundes zurueck.'''
        ...

    def verbund_loeschen(self, id: int) -> None:
        '''loescht den Verbund logisch.'''
        ...

    def verbund_mitglied_hinzu(self, verbund_id: int, person_id: int, rolle: str) -> None:
        '''fuegt die Person zur angegebenen ID dem Verbund hinzu.'''
        ...

    def verbund_mitglied_entfernen(self, verbund_id: int, person_id: int, rolle: str = None) -> None:
        '''entfernt die Person zur angegebenen ID aus dem Verbund.'''
        ...


class KontenManager(Protocol):
    '''Interface zur Verwaltung von Konten'''

    def konto_lesen(self, konto_id: int) -> Konto:
        '''Liest die Kontodaten zum angegebenen Konto'''
        ...

    def konten_zu_person_lesen(self, person_id: int) -> Sequence[Konto]:
        '''Ermittelt alle Konten zu einer Person'''
        ...

    def konto_anlegen(self, person_id: int, prod_var: str) -> Konto:
        '''Legt ein neues Konto mit der gegebenen Produktvariante ::prod_var an.'''
        ...

    def konto_loeschen(self, konto_id: int) -> None:
        '''Loescht bzw. historisiert das angegebene Konto.'''
        ...

    def buchen(self, buchtext: str, ktn_betraege: Sequence[BuchSatz], valuta: date = None) -> None:
        '''Fuehrt eine Buchung durch'''
        ...

    def buchungen_lesen(self, konto_id: int) -> Umsatz:
        '''Liest die Buchungen zum angegebenen Konto'''
        ...
        
    def konto_kuendigen(self, kto_id: int, kdg_datum: date) -> Konto:
        '''Kündigt das Konto'''