from typing import Sequence

import ttkbootstrap as ttb
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.tooltip import ToolTip

from model.controller import Controller
from model.person import Person


class PersonenListeFrame(ttb.Frame):
    '''Ein Frame zur Anzeige einer Personenliste'''

    def __init__(self, master, controller: Controller):
        super().__init__(master=master)
        self.controller: Controller = controller

        self._build_ui()
        self._register_bindings()

    def _build_ui(self):
        self._suchfeld_frm = ttb.LabelFrame(
            self, text="Namen eingeben", bootstyle='primary')
        self._suchfeld_frm.pack(padx=10, pady=10, side='top', fill='x')

        self._suchfeld = ttb.Entry(self._suchfeld_frm, width=50)
        self._suchfeld_tt = ToolTip(
            self._suchfeld, text="Suche mit <Return> starten")

        self._suchfeld.pack(padx=10, pady=10, side='left', fill='x')

        self._btn_suche_starten = ttb.Button(
            self._suchfeld_frm, text="Suche starten")
        self._btn_suche_starten.pack(padx=10, pady=10, side='left')

        self._trefferliste_frm = ttb.LabelFrame(
            self, text="Treffer", bootstyle='primary')
        self._trefferliste_frm.pack(
            padx=10, pady=10, side='top', fill='both', expand=True)

        self._treffer = Tableview(self._trefferliste_frm, coldata=[
                                  "Personen"], paginated=True)
        self._treffer_tt = ToolTip(
            self._treffer, text='Person per Doppelklick auswählen')
        self._treffer.pack(padx=10, pady=10, side='top',
                           fill='both', expand=True)
        self._treffer.view.column('#1', width=400, stretch=True)

    def _register_bindings(self) -> None:
        self._suchfeld.bind(
            '<Return>', lambda e: self.controller.personen_suchen(self._suchfeld.get()))

        self._btn_suche_starten.configure(
            command=lambda: self.controller.personen_suchen(self._suchfeld.get()))

        self._treffer.view.bind('<Double-Button-1>',
                                self._on_doubleclick_person)

        self.controller.register(
            self.controller.EVT_PERSONEN_SUCHEN, self.on_update_personenliste)

        self.bind("<KeyPress>", lambda e: print("Gedrückt"))

    def _on_doubleclick_person(self, e) -> None:
        '''Reagiert auf den Doppelklick auf einen Eintrag in der Personenliste'''
        sel = self._treffer.view.selection()
        id = int(self._treffer.view.item(sel)['values'][1])
        self.controller.personendetails_anzeigen(id)

    def on_update_personenliste(self, p_liste: Sequence[Person]) -> None:
        '''Aktualisiert die Personenliste'''

        self._treffer.delete_rows()

        for p in p_liste:
            zeile = f"{p.id} - {p.nachname}"
            if p.vorname:
                zeile = zeile + f", {p.vorname}"

            self._treffer.insert_row('end', [zeile, p.id])

        self._treffer.load_table_data(clear_filters=True)

    def show(self) -> None:
        self.tkraise()
        self._suchfeld.focus()
        self.master.top = self

    def on_cancel(self) -> None:
        '''Wenn Abbruch gesendet wird'''
        self.controller.personenliste_anzeigen()