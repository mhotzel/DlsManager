import locale
from datetime import datetime
from tkinter import StringVar

from ttkbootstrap import (Button, DateEntry, Entry, Frame, Label, LabelFrame,
                          Separator)

from model.controller import Controller
from model.db_manager import BuchSatz


class BuchungsmaskeFrm(Frame):

    def __init__(self, master, controller: Controller) -> None:
        super().__init__(master)

        self.controller = controller
        self._data = {
            'buchtext': StringVar(),
            'kto': [],
            'inhaber': [],
            'ts': [],
            'betrag': []
        }

        for i in range(4):
            self._data['kto'].append(StringVar())
            self._data['inhaber'].append(StringVar())
            self._data['ts'].append(StringVar())
            self._data['betrag'].append(StringVar())

        self._build_ui()
        self._register_bindings()

    def _build_ui(self) -> None:

        self._frm_buchkopf = LabelFrame(
            self, text='Buchungsdaten', bootstyle='primary')
        self._frm_buchkopf.pack(fill='x', padx=10, pady=10)

        self.lbl_valuta = Label(self._frm_buchkopf, text='Valuta:')
        self.lbl_valuta.grid(row=0, column=0, sticky='E', padx=10, pady=10)

        self.fld_valuta = DateEntry(
            self._frm_buchkopf, width=10, dateformat='%d.%m.%Y', firstweekday=0)
        self.fld_valuta.grid(row=0, column=1, padx=10, pady=10, sticky='W')

        self.lbl_buchtext = Label(self._frm_buchkopf, text='Buchungstext:')
        self.lbl_buchtext.grid(row=1, column=0, padx=10, pady=10, sticky='E')

        self.fld_buchtext = Entry(
            self._frm_buchkopf, textvariable=self._data['buchtext'], width=40)
        self.fld_buchtext.grid(row=1, column=1, sticky='W', padx=10, pady=10)

        # ----------------------

        self._frm_buchungsdaten = LabelFrame(
            self, text='Buchungsdaten', bootstyle='primary')
        self._frm_buchungsdaten.pack(fill='x', padx=10, pady=10)

        self.lbl_kto = Label(
            self._frm_buchungsdaten, text='Konto', width=10, font=('', '9', 'bold'))
        self.lbl_kto.grid(row=0, column=0, sticky='E', padx=10, pady=5)

        self.lbl_name = Label(
            self._frm_buchungsdaten, text='Name Inhaber', width=30, font=('', '9', 'bold'))
        self.lbl_name.grid(row=0, column=1, sticky='E', padx=10, pady=5)

        self.lbl_ts = Label(
            self._frm_buchungsdaten, text='TS', width=6, font=('', 9, 'bold'))
        self.lbl_ts.grid(row=0, column=2, sticky='E', padx=10, pady=5)

        self.lbl_betrag = Label(
            self._frm_buchungsdaten, text='Betrag', width=20, font=('', 9, 'bold'))
        self.lbl_betrag.grid(row=0, column=3, sticky='E', padx=10, pady=5)

        self.sep = Separator(
            self._frm_buchungsdaten, orient='horizontal', bootstyle='primary')
        self.sep.grid(row=1, column=0, columnspan=4,
                      sticky='WE', padx=10, pady=5)

        self.fld_kto1 = Entry(
            self._frm_buchungsdaten, textvariable=self._data['kto'][0], width=10)
        self.fld_kto1.grid(row=5, column=0, sticky='WE', padx=10, pady=5)

        self.fld_name1 = Entry(
            self._frm_buchungsdaten, textvariable=self._data['inhaber'][0], width=30, state='readonly')
        self.fld_name1.grid(row=5, column=1, sticky='WE', padx=10, pady=5)

        self.fld_ts1 = Entry(
            self._frm_buchungsdaten, textvariable=self._data['ts'][0], width=6)
        self.fld_ts1.grid(row=5, column=2, sticky='WE', padx=10, pady=5)

        self.fld_betr1 = Entry(
            self._frm_buchungsdaten, textvariable=self._data['betrag'][0], width=20)
        self.fld_betr1.grid(row=5, column=3, sticky='WE', padx=10, pady=5)

        self.fld_kto2 = Entry(
            self._frm_buchungsdaten, textvariable=self._data['kto'][1], width=10)
        self.fld_kto2.grid(row=6, column=0, sticky='WE', padx=10, pady=5)

        self.fld_name2 = Entry(
            self._frm_buchungsdaten, textvariable=self._data['inhaber'][1], width=30, state='readonly')
        self.fld_name2.grid(row=6, column=1, sticky='WE', padx=10, pady=5)

        self.fld_ts2 = Entry(
            self._frm_buchungsdaten, textvariable=self._data['ts'][1], width=6)
        self.fld_ts2.grid(row=6, column=2, sticky='WE', padx=10, pady=5)

        self.fld_betr2 = Entry(
            self._frm_buchungsdaten, textvariable=self._data['betrag'][1], width=20)
        self.fld_betr2.grid(row=6, column=3, sticky='WE', padx=10, pady=5)

        self.fld_kto3 = Entry(
            self._frm_buchungsdaten, textvariable=self._data['kto'][2], width=10)
        self.fld_kto3.grid(row=7, column=0, sticky='WE', padx=10, pady=5)

        self.fld_name3 = Entry(
            self._frm_buchungsdaten, textvariable=self._data['inhaber'][2], width=30, state='readonly')
        self.fld_name3.grid(row=7, column=1, sticky='WE', padx=10, pady=5)

        self.fld_ts3 = Entry(
            self._frm_buchungsdaten, textvariable=self._data['ts'][2], width=6)
        self.fld_ts3.grid(row=7, column=2, sticky='WE', padx=10, pady=5)

        self.fld_betr3 = Entry(
            self._frm_buchungsdaten, textvariable=self._data['betrag'][2], width=20)
        self.fld_betr3.grid(row=7, column=3, sticky='WE', padx=10, pady=5)

        self.fld_kto4 = Entry(
            self._frm_buchungsdaten, textvariable=self._data['kto'][3], width=10)
        self.fld_kto4.grid(row=8, column=0, sticky='WE', padx=10, pady=5)

        self.fld_name4 = Entry(
            self._frm_buchungsdaten, textvariable=self._data['inhaber'][3], width=30, state='readonly')
        self.fld_name4.grid(row=8, column=1, sticky='WE', padx=10, pady=5)

        self.fld_ts4 = Entry(
            self._frm_buchungsdaten, textvariable=self._data['ts'][3], width=6)
        self.fld_ts4.grid(row=8, column=2, sticky='WE', padx=10, pady=5)

        self.fld_betr4 = Entry(
            self._frm_buchungsdaten, textvariable=self._data['betrag'][3], width=20)
        self.fld_betr4.grid(row=8, column=3, sticky='WE', padx=10, pady=5)

        self.lbl_blind_soll = Label(self._frm_buchungsdaten)
        self.lbl_blind_soll.grid(row=9, column=0)

        # ----------------------

        self._frm_buttons = Frame(self)
        self._frm_buttons.pack(fill='x', padx=10, pady=10)

        self.btn_buchen = Button(
            self._frm_buttons, text='Buchen', bootstyle='secondary')
        self.btn_buchen.pack(side='right', padx=10, pady=10)

        self.btn_check_ktn = Button(
            self._frm_buttons, text='Konten prüfen', bootstyle='secondary')
        self.btn_check_ktn.pack(side='right', padx=10, pady=10)

        self.btn_maske_leeren = Button(self._frm_buttons, text='Maske leeren', bootstyle='secondary')
        self.btn_maske_leeren.pack(side='right', padx=10, pady=10)

    def _register_bindings(self) -> None:
        self.btn_check_ktn.configure(command=self._on_check_ktn)
        self.btn_buchen.configure(command=self._on_buchen)
        self.btn_maske_leeren.configure(command=self._on_maske_leeren)

    def _on_maske_leeren(self) -> None:
        
        self._data['buchtext'].set("")

        for i, _ in enumerate(self._data['kto']):
            self._data['kto'][i].set("")
            self._data['inhaber'][i].set("")
            self._data['ts'][i].set("")
            self._data['betrag'][i].set("")
            

    def _on_buchen(self) -> None:
        '''Führt die Buchung durch'''

        buchsaetze = []
        for i, _ in enumerate(self._data['kto']):
            if self._data['kto'][i].get() == "" or self._data['kto'][i].get() == 0:
                continue
            buchsaetze.append(BuchSatz(
                kto=self._get_default_int(self._data['kto'][i].get(), 0),
                schluessel=self._get_default_int(self._data['ts'][i].get(), 0),
                betrag=locale.atof(self._data['betrag'][i].get())
            ))

        buchtext = self._data['buchtext'].get()
        valuta = datetime.strptime(
            self.fld_valuta.entry.get(), '%x').date()

        self.controller.buchen(buchtext=buchtext, valuta=valuta, ktn_betraege=buchsaetze)
       
    def _on_check_ktn(self) -> None:
        '''Prüft die Konten auf Existenz und ergänzt die Namen der Inhaber'''

        buchsaetze = []
        for i, _ in enumerate(self._data['kto']):
            buchsaetze.append(BuchSatz(
                kto=self._get_default_int(self._data['kto'][i].get(), 0),
                schluessel=self._get_default_int(self._data['ts'][i].get(), 0),
                betrag=self._get_default_float(
                    self._data['betrag'][i].get(), 0.0)
            ))
        
        inhaber = self.controller.pruefe_konten(buchsaetze)
        for i, inh in enumerate(inhaber):
            self._data['inhaber'][i].set(inh)

    def show(self) -> None:
        self._on_maske_leeren()
        self.tkraise()
        self.master.top = self

    def _get_default_int(self, wert: str, default: int = 0) -> int:
        try:
            return int(wert)
        except:
            return default

    def _get_default_float(self, wert: str, default: float = 0.0) -> int:
        try:
            return float(wert)
        except:
            return default

    def on_cancel(self) -> None:
        '''Wenn Abbruch gesendet wird'''
        self.controller.personenliste_anzeigen()