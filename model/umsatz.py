from dataclasses import dataclass
from datetime import date, datetime


@dataclass(eq=True, frozen=True)
class Umsatz():
    kto: int
    von: datetime
    buchtag: date
    valuta: date
    buchtext: str
    schluessel: int
    betrag: float
    buch_id: int
