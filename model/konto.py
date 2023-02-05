from dataclasses import dataclass
from datetime import date
from hashlib import sha256


@dataclass(eq=True)
class Konto():
    '''Ein Konto'''

    id: int = None
    inh_id: int = None
    inh_name: str = None
    prod_var: str = None
    gekuendigt: date = None
    saldo: float = None

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False

        other: Konto = __o
        h1 = _hash_kto(self)
        h2 = _hash_kto(other)

        return h1 == h2


def _hash_kto(k: Konto) -> str:
    return sha256(f'{k.id}-{k.inh_id}-{k.inh_name}-{k.prod_var}-{k.gekuendigt}'.encode()).hexdigest()
