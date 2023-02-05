from tkinter import StringVar
from typing import Sequence

from ttkbootstrap import Button, Combobox, Entry, Frame, Label, LabelFrame

from model.controller import Controller
from model.person import Person


class KontoAnlegenFrm(Frame):
    '''Bildschirm zur Kontoanlage'''

    def __init__(self, master, controller: Controller):
        super().__init__(master)
        self.controller: Controller = controller
        self.person: Person = None

        self._data = {
            'person': StringVar(),
            'prodvar': StringVar()
        }

        self._build_ui()
        self._register_bindings()

    def _build_ui(self) -> None:
        self._frm_personendaten = LabelFrame(
            self, text='Personendaten', bootstyle='primary')
        self._frm_personendaten.pack(fill='x', padx=10, pady=10)

        self.lbl_person = Label(self._frm_personendaten, text='Person:')
        self.lbl_person.grid(row=0, column=0, sticky='E', padx=10, pady=10)

        self.fld_person = Entry(
            self._frm_personendaten, state='readonly', textvariable=self._data['person'], width=40)
        self.fld_person.grid(row=0, column=1, sticky='W', padx=10, pady=10)

        self._frm_kontodaten = LabelFrame(
            self, text='Kontodaten', bootstyle='primary')
        self._frm_kontodaten.pack(fill='x', padx=10, pady=10)

        self.lbl_produkt = Label(self._frm_kontodaten,
                                 text='Kontoart auswählen:')
        self.lbl_produkt.grid(row=0, column=0, sticky='E', padx=10, pady=10)

        self.cmb_produkt = Combobox(
            self._frm_kontodaten, textvariable=self._data['prodvar'], width=40, state='readonly')
        self.cmb_produkt.grid(row=0, column=1, sticky='W', padx=10, pady=10)

        self.btn_kontoanlegen = Button(
            self._frm_kontodaten, text='Konto anlegen', bootstyle='secondary')
        self.btn_kontoanlegen.grid(
            row=0, column=2, padx=10, pady=10, sticky='WE')

    def _register_bindings(self) -> None:
        self.cmb_produkt.bind('<<ComboboxSelected>>',
                              lambda x: self.cmb_produkt.selection_clear())
        self.btn_kontoanlegen.configure(command=self._on_konto_anlegen_click)

    def _on_konto_anlegen_click(self) -> None:
        if len(self._data['prodvar'].get()) < 1:
            self.controller.nachricht_anzeigen(
                "Kontoanlage ist nich möglich, da keine Produktart gewählt wurde")
            return

        self.controller.konto_anlegen(
            self.person.id, self._data['prodvar'].get())

    def show(self, person: Person, produktauswahl: Sequence[str]) -> None:
        self.person = person
        name = f"{person.nachname}"
        if person.vorname:
            name += ", " + f"{person.vorname}"
        self._data['prodvar'].set("")
        self._data['person'].set(f"{person.id} - {name}")
        self.cmb_produkt.configure(values=produktauswahl)
        self.tkraise()
        self.master.top = self

    def on_cancel(self) -> None:
        '''Wenn Abbruch gesendet wird'''
        self.controller.personendetails_anzeigen(self.person.id)
