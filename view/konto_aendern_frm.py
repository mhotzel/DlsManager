import locale
from tkinter import StringVar

from ttkbootstrap import (Button, DateEntry, Entry, Frame, Label, LabelFrame,
                          Toplevel)

from model.controller import Controller
from model.konto import Konto


class KontoAendernFrm(Toplevel):

    def __init__(self, master, konto: Konto, controller: Controller):
        super().__init__(title='Konto ändern', master=master)

        self.controller = controller
        self.konto = konto

        self._data = {
            'konto_id': StringVar(),
            'inhaber': StringVar(),
            'prod_var': StringVar(),
            'gekuendigt': StringVar(),
            'saldo': StringVar()
        }

        self._fill_form()
        self._build_ui()

    def _fill_form(self) -> None:
        self._data['konto_id'].set(str(self.konto.id))
        self._data['inhaber'].set(self.konto.inh_name)
        self._data['prod_var'].set(self.konto.prod_var)
        self._data['gekuendigt'].set(self.konto.gekuendigt.strftime('%x') if self.konto.gekuendigt else '')
        self._data['saldo'].set(f"{locale.currency(self.konto.saldo, grouping=True, symbol='')} EUR")

    def _build_ui(self) -> None:
        self.transient(self.master)

        self._frm_kopfdaten = LabelFrame(
            self, text='Kontodaten ändern', bootstyle='primary')
        self._frm_kopfdaten.pack(fill='both', expand=True, padx=10, pady=10)

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

        self.fld_gekuendigt = DateEntry(
            self._frm_kopfdaten, width=10, firstweekday=0)
        self.fld_gekuendigt.entry.configure(
            textvariable=self._data['gekuendigt'])
        self.fld_gekuendigt.grid(row=1, column=1, padx=10, pady=10, sticky='W')

        self._frm_btns = Frame(self)
        self._frm_btns.pack(fill='both', expand=True, padx=10, pady=10)

        self.btn_speichern = Button(
            self._frm_btns, text="Speichern", bootstyle='secondary', command=self.kuendigen)
        self.btn_speichern.pack(side='right', padx=10, pady=10)

        self.btn_cancel = Button(
            self._frm_btns, text="Abbrechen", bootstyle='secondary', command=self.ausblenden)
        self.btn_cancel.pack(side='right', padx=10, pady=10)

        self.bind('<KeyPress-Escape>', lambda e: self.ausblenden())

        self.position_center()
        self.wait_visibility()

        self.grab_set()
        self.wait_window()

    def kuendigen(self) -> None:
        self.controller.konto_aendern(self._data['konto_id'].get(), self._data['gekuendigt'].get())
        self.ausblenden()

    def ausblenden(self) -> None:
        self.grab_release()
        self.destroy()
