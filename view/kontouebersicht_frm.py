import locale
from tkinter import StringVar
from typing import Sequence

from ttkbootstrap import Button, Entry, Frame, Label, LabelFrame, Separator
from ttkbootstrap.tableview import Tableview

from model.controller import Controller
from model.konto import Konto
from model.umsatz import Umsatz


class KontouebersichtFrm(Frame):
    '''Zeigt die Kontoübersicht zu einem Konto an.'''

    def __init__(self, master, controller: Controller):
        super().__init__(master)

        self.controller = controller
        self._data = {
            'konto_id': StringVar(),
            'inhaber': StringVar(),
            'inhaber': StringVar(),
            'prod_var': StringVar(),
            'gekuendigt': StringVar(),
            'saldo': StringVar()
        }

        self._build_ui()
        self._register_bindings()

    def _build_ui(self) -> None:
        self._frm_konto_uebersicht = LabelFrame(
            self, text='Kontoübersicht', bootstyle='primary')
        self._frm_konto_uebersicht.pack(side='top', fill='x', padx=10, pady=10)

        self._frm_kopfdaten = Frame(self._frm_konto_uebersicht)
        self._frm_kopfdaten.grid(row=0, column=0, sticky='WE')

        self.lbl_konto = Label(self._frm_kopfdaten, text='Konto:')
        self.lbl_konto.grid(row=0, column=0, sticky='E', padx=10, pady=10)

        self.fld_konto = Entry(self._frm_kopfdaten,
                               textvariable=self._data['konto_id'], state='readonly', width=10)
        self.fld_konto.grid(row=0, column=1, sticky='W', padx=10, pady=10)

        self.lbl_inhaber = Label(self._frm_kopfdaten, text='Inhaber:')
        self.lbl_inhaber.grid(row=0, column=2, sticky='E', padx=10, pady=10)

        self.fld_inhaber = Entry(
            self._frm_kopfdaten, textvariable=self._data['inhaber'], state='readonly')
        self.fld_inhaber.grid(row=0, column=3, sticky='W', padx=10, pady=10)

        self.lbl_saldo = Label(self._frm_kopfdaten, text='Saldo:')
        self.lbl_saldo.grid(row=0, column=4, sticky='E', padx=10, pady=10)

        self.fld_saldo = Entry(
            self._frm_kopfdaten, textvariable=self._data['saldo'], state='readonly')
        self.fld_saldo.grid(row=0, column=5, sticky='W', padx=10, pady=10)

        self.lbl_gekuendigt = Label(
            self._frm_kopfdaten, text='Kündigungsdatum:')
        self.lbl_gekuendigt.grid(row=1, column=0, sticky='E', padx=10, pady=10)

        self.fld_gekuendigt = Entry(
            self._frm_kopfdaten, textvariable=self._data['gekuendigt'], state='readonly', width=10)
        self.fld_gekuendigt.grid(row=1, column=1, padx=10, pady=10, sticky='W')

        self.sep = Separator(self._frm_konto_uebersicht,
                             orient='horizontal', bootstyle='primary')
        self.sep.grid(row=2, column=0,
                      padx=10, pady=10, sticky='WE')

        self.umsatzliste = Tableview(self._frm_konto_uebersicht, coldata=[
                                     'Buch.-Tag', 'Valuta', 'Buch.-Text', 'Schl.', 'Betrag'], paginated=True, height=10, pagesize=10)
        self.umsatzliste.view.column('#3', stretch=True)
        self.umsatzliste.align_column_right(cid=4)
        self.umsatzliste.grid(row=3, column=0,
                              padx=10, pady=10, sticky='WE')

        self._btnleiste = Frame(self)
        self._btnleiste.pack(side='top', padx=10, pady=10, fill='x')

        self.btn_personendetails = Button(
            self._btnleiste, text='Zurück zur Personananzeige', bootstyle='secondary')
        self.btn_personendetails.pack(side='right', padx=10, pady=10)

        self.btn_kuendigen = Button(
            self._btnleiste, text="Kündigungsdatum setzen", bootstyle='secondary')
        self.btn_kuendigen.pack(side='right', padx=10, pady=10)

    def _register_bindings(self) -> None:
        self.btn_personendetails.configure(
            command=lambda: self.controller.personendetails_anzeigen(self.konto.inh_id))
        self.btn_kuendigen.configure(
            command=lambda: self.controller.konto_aendern_anzeigen(self.konto.id))

    def show(self, konto: Konto, umsaetze: Sequence[Umsatz]) -> None:
        self.konto = konto
        self.umsaetze: Sequence[Umsatz] = umsaetze
        self._fill_form()
        self.tkraise()
        self.master.top = self

    def _fill_form(self) -> None:
        self._data['konto_id'].set(self.konto.id)
        self._data['inhaber'].set(
            f"{self.konto.inh_id} - {self.konto.inh_name}")
        self._data['prod_var'].set(self.konto.prod_var)
        self._data['gekuendigt'].set(
            self.konto.gekuendigt.strftime('%x') if self.konto.gekuendigt else '')
        self._data['saldo'].set(
            f"{locale.currency(self.konto.saldo, grouping=True, symbol='')} EUR")

        self.umsatzliste.delete_rows()
        for umsatz in self.umsaetze:
            self.umsatzliste.insert_row('end', values=[umsatz.buchtag.strftime('%x'), umsatz.valuta.strftime('%x'), umsatz.buchtext,
                                        umsatz.schluessel, f"{locale.currency(umsatz.betrag, grouping=True, symbol='')} EUR"])

        self.umsatzliste.load_table_data(clear_filters=True)

    def on_cancel(self) -> None:
        '''Wenn Abbruch gesendet wird'''
        self.controller.personendetails_anzeigen(self.konto.inh_id)