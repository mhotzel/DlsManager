from dataclasses import dataclass


@dataclass(eq=True)
class Verbund():
    '''a person'''

    VERBUNDTYPEN = set(('Eheleute', 'Sonstige', 'Vertreter'))

    VERBUNDROLLEN = set(('Ehemann', 'Ehefrau', 'Ansprechpartner',
                        'Vorsitzender', 'Vorstand', 'Geschäftsführer'))

    id: int = None
    typ: str = None

    def __hash__(self) -> int:
        return hash(self.id)
