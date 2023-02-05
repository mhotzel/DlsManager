from dataclasses import dataclass
from datetime import date
from hashlib import sha256


@dataclass(eq=True)
class Person():
    '''a person'''

    id: int = None
    typ: str = None
    anrede: str = None
    titel: str = None
    nachname: str = None
    vorname: str = None
    geboren: date = None
    verstorben: date = None
    gekuendigt: date = None
    post_erg: str = None
    strasse: str = None
    plz: str = None
    ort: str = None
    land: str = None
    tel1: str = None
    tel2: str = None
    email: str = None
    kdnr: str = None
    hinweise: str = None

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False

        other: Person = __o
        h1 = _hash_person(self)
        h2 = _hash_person(other)

        return h1 == h2


def _hash_person(p: Person) -> str:
    return sha256(f'{p.id}-{p.typ}-{p.anrede}-{p.titel}-{p.nachname}-{p.vorname}-{p.geboren}-{p.verstorben}-{p.gekuendigt}-{p.post_erg}-{p.strasse}-{p.plz}-{p.ort}-{p.land}-{p.tel1}-{p.tel2}-{p.email}-{p.kdnr}-{p.hinweise}'.encode()).hexdigest()
