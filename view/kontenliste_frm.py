import locale
from typing import Sequence

import ttkbootstrap as ttb
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.tooltip import ToolTip

from model.controller import Controller
from model.konto import Konto


class KontenListeFrm(ttb.LabelFrame):

    def __init__(self, master, controller: Controller) -> None:
        super().__init__(master, text='Kontenliste', bootstyle='primary')
        self.controller = controller

        self._konten: Sequence[Konto] = None

        self._build_ui()
        self._register_bindings()

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.tabelle = Tableview(self, coldata=['Konto', 'Saldo'], height=3, autoalign=True)
        self.tabelle.align_column_right(cid=1)
        self.tabelle.view.column('#1', stretch=True)
        self.tabelle.pack(expand=True, fill='both', padx=10, pady=10)

        self.tabelle_tt = ToolTip(self.tabelle, text='Konto per Doppelklick auswählen')

    def _fill_form(self) -> None:
        self.tabelle.delete_rows()

        for kto in self._konten:
            self.tabelle.insert_row('end', [f"{kto.id} - {kto.prod_var}", f"{locale.currency(kto.saldo, grouping=True, symbol='')} EUR", kto.id])

        self.tabelle.load_table_data(clear_filters=True)

    def _register_bindings(self) -> None:
        self.tabelle.view.bind('<Double-Button-1>',
                        self._on_doubleclick_konto)

    def _on_doubleclick_konto(self, *args) -> None:
        '''Reagiert auf den Doppelklick auf einen Eintrag in der Personenliste'''
        sel = self.tabelle.view.selection()
        ktoid = int(self.tabelle.view.item(sel)['values'][2])
        self.controller.kontouebersicht_anzeigen(ktoid)

    @property
    def konten(self) -> Sequence[Konto]:
        return self.konten

    @konten.setter
    def konten(self, konten: Sequence[Konto]) -> None:
        self._konten = konten
        self._fill_form()
