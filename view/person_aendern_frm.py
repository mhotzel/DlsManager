from datetime import date, datetime
from tkinter import StringVar

import ttkbootstrap as ttb
from ttkbootstrap.scrolled import ScrolledText

from model.controller import Controller
from model.person import Person


class PersonAendernFrame(ttb.Frame):
    '''Bildschirm zum Ändern der Personendaten'''

    def __init__(self, master, controller: Controller) -> None:
        super().__init__(master=master)
        self.controller = controller

        self.data = {k: StringVar() for k in ['person_id', 'typ', 'anrede', 'titel', 'nachname', 'vorname',
                                              'geboren', 'verstorben', 'gekuendigt', 'post_erg', 'strasse', 'plz', 'ort', 'land', 'tel1', 'tel2', 'email', 'kdnr']}

        self._build_ui()
        self._register_bindings()

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)

        self._frm_persdet = ttb.LabelFrame(
            self, text='Details zur Person', bootstyle='primary')
        self._frm_persdet.grid(
            row=0, column=0, sticky='NWES', padx=10, pady=10)

        self.lbl_person_id = ttb.Label(
            self._frm_persdet, text='Personen-ID:')
        self.lbl_person_id.grid(row=0, column=0, padx=10, pady=10, sticky='E')

        self.fld_person_id = ttb.Entry(
            self._frm_persdet, width=10, textvariable=self.data['person_id'])
        self.fld_person_id.grid(row=0, column=1, padx=10, pady=10, sticky='WE')

        self.lbl_kdnr = ttb.Label(self._frm_persdet, text='Kdnr:')
        self.lbl_kdnr.grid(row=0, column=2, padx=10, pady=10, sticky='E')

        self.fld_kdnr = ttb.Entry(
            self._frm_persdet, width=10, textvariable=self.data['kdnr'])
        self.fld_kdnr.grid(row=0, column=3, padx=10, pady=10, sticky='WE')

        self.lbl_typ = ttb.Label(self._frm_persdet, text='Personentyp:')
        self.lbl_typ.grid(row=1, column=0, padx=10, pady=10, sticky='E')

        self.fld_typ = ttb.Combobox(
            self._frm_persdet, state='readonly', width=10, textvariable=self.data['typ'], values=['P - Einzelperson', 'G - Gemeinschaftsperson', 'J - Jur. Person'])
        self.fld_typ.grid(row=1, column=1, columnspan=3,
                          padx=10, pady=10, sticky='WE')

        self.lbl_anrede = ttb.Label(self._frm_persdet, text='Anrede:')
        self.lbl_anrede.grid(row=2, column=0, sticky='E', padx=10, pady=10)

        self.fld_anrede = ttb.Entry(
            self._frm_persdet, textvariable=self.data['anrede'])
        self.fld_anrede.grid(row=2, column=1, columnspan=3,
                             padx=10, pady=10, sticky='WE')

        self.lbl_titel = ttb.Label(self._frm_persdet, text='Titel:')
        self.lbl_titel.grid(row=3, column=0, sticky='E', padx=10, pady=10)

        self.fld_titel = ttb.Entry(
            self._frm_persdet, textvariable=self.data['titel'])
        self.fld_titel.grid(row=3, column=1, columnspan=3,
                            padx=10, pady=10, sticky='WE')

        self.lbl_nachname = ttb.Label(self._frm_persdet, text='Nachname:')
        self.lbl_nachname.grid(row=4, column=0, sticky='E', padx=10, pady=10)

        self.fld_nachname = ttb.Entry(
            self._frm_persdet, textvariable=self.data['nachname'])
        self.fld_nachname.grid(row=4, column=1, columnspan=3,
                               padx=10, pady=10, sticky='WE')

        self.lbl_vorname = ttb.Label(self._frm_persdet, text='Vorname:')
        self.lbl_vorname.grid(row=5, column=0, sticky='E', padx=10, pady=10)

        self.fld_vorname = ttb.Entry(
            self._frm_persdet, textvariable=self.data['vorname'])
        self.fld_vorname.grid(row=5, column=1, columnspan=3,
                              padx=10, pady=10, sticky='WE')

        self.lbl_geboren = ttb.Label(self._frm_persdet, text='Geboren:')
        self.lbl_geboren.grid(row=6, column=0, sticky='E', padx=10, pady=10)

        self.fld_geboren = ttb.Entry(
            self._frm_persdet, width=10, textvariable=self.data['geboren'])
        self.fld_geboren.grid(row=6, column=1, padx=10, pady=10, sticky='WE')

        self.lbl_verstorben = ttb.Label(self._frm_persdet, text='Verstorben:')
        self.lbl_verstorben.grid(row=6, column=2, sticky='E', padx=10, pady=10)

        self.fld_verstorben = ttb.Entry(
            self._frm_persdet, width=10, textvariable=self.data['verstorben'])
        self.fld_verstorben.grid(
            row=6, column=3, padx=10, pady=10, sticky='WE')

        self._frm_adr = ttb.LabelFrame(
            self, text="Adress- und Kontaktdaten", bootstyle='primary')
        self._frm_adr.grid(row=0, column=1, sticky='NWES', padx=10, pady=10)

        self.lbl_posterg = ttb.Label(self._frm_adr, text='Post. Ergänzung:')
        self.lbl_posterg.grid(row=0, column=0, sticky='E', padx=10, pady=10)

        self.fld_posterg = ttb.Entry(
            self._frm_adr, width=36, textvariable=self.data['post_erg'])
        self.fld_posterg.grid(row=0, column=1, columnspan=3,
                              sticky='WE', padx=10, pady=10)

        self.lbl_strasse = ttb.Label(self._frm_adr, text='Strasse:')
        self.lbl_strasse.grid(row=1, column=0, sticky='E', padx=10, pady=10)

        self.fld_strasse = ttb.Entry(
            self._frm_adr, width=36, textvariable=self.data['strasse'])
        self.fld_strasse.grid(row=1, column=1, columnspan=3,
                              sticky='WE', padx=10, pady=10)

        self.lbl_land = ttb.Label(self._frm_adr, text='Land:')
        self.lbl_land.grid(row=2, column=0, sticky='E', padx=10, pady=10)

        self.fld_land = ttb.Entry(
            self._frm_adr, width=6, textvariable=self.data['land'])
        self.fld_land.grid(row=2, column=1, sticky='WE', padx=10, pady=10)

        self.lbl_plz = ttb.Label(self._frm_adr, text='PLZ:')
        self.lbl_plz.grid(row=2, column=2, sticky='E', padx=10, pady=10)

        self.fld_plz = ttb.Entry(
            self._frm_adr, width=6, textvariable=self.data['plz'])
        self.fld_plz.grid(row=2, column=3, sticky='WE', padx=10, pady=10)

        self.lbl_ort = ttb.Label(self._frm_adr, text='Ort:')
        self.lbl_ort.grid(row=3, column=0, sticky='E', padx=10, pady=10)

        self.fld_ort = ttb.Entry(
            self._frm_adr, width=36, textvariable=self.data['ort'])
        self.fld_ort.grid(row=3, column=1, columnspan=3,
                          sticky='WE', padx=10, pady=10)

        self.sep_kontaktdaten = ttb.Separator(
            self._frm_adr, orient='horizontal', bootstyle='primary')
        self.sep_kontaktdaten.grid(
            row=4, column=0, columnspan=4, padx=10, pady=10, sticky='WE')

        self.lbl_tel1 = ttb.Label(self._frm_adr, text='Tel 1:')
        self.lbl_tel1.grid(row=5, column=0, sticky='E', padx=10, pady=10)

        self.fld_tel1 = ttb.Entry(
            self._frm_adr, width=36, textvariable=self.data['tel1'])
        self.fld_tel1.grid(row=5, column=1, columnspan=3,
                           sticky='WE', padx=10, pady=10)

        self.lbl_tel2 = ttb.Label(self._frm_adr, text='Tel 2:')
        self.lbl_tel2.grid(row=6, column=0, sticky='E', padx=10, pady=10)

        self.fld_tel2 = ttb.Entry(
            self._frm_adr, width=36, textvariable=self.data['tel2'])
        self.fld_tel2.grid(row=6, column=1, columnspan=3,
                           sticky='WE', padx=10, pady=10)

        self.lbl_email = ttb.Label(self._frm_adr, text='E-Mail:')
        self.lbl_email.grid(row=7, column=0, sticky='E', padx=10, pady=10)

        self.fld_email = ttb.Entry(
            self._frm_adr, width=36, textvariable=self.data['email'])
        self.fld_email.grid(row=7, column=1, columnspan=3,
                            sticky='WE', padx=10, pady=10)

        self._frm_hinweise = ttb.LabelFrame(
            self, text='Hinweise',  bootstyle='primary')
        self._frm_hinweise.grid(
            row=1, column=0, padx=10, pady=10, sticky='NWES')

        self.fld_hinweise = ScrolledText(
            self._frm_hinweise, height=5, width=40)
        self.fld_hinweise.pack(fill='both', expand=True, padx=10, pady=10)

        self._frm_btns = ttb.Frame(
            self, borderwidth=1, relief='flat', border=1)
        self._frm_btns.grid(row=2, column=0, columnspan=2,
                            padx=10, pady=10, sticky='NSWE')
        self._frm_btns.columnconfigure(1, weight=1)


        self.btn_save = ttb.Button(
            self._frm_btns, text='Änderungen speichern', bootstyle='secondary')
        self.btn_save.pack(side='right', padx=10, pady=10)

        self.btn_cancel = ttb.Button(
            self._frm_btns, text='Abbrechen', bootstyle='secondary')
        self.btn_cancel.pack(side='right', padx=10, pady=10)

    def _register_bindings(self) -> None:
        self.btn_cancel.configure(
            command=self._on_cancel_btn)

        self.fld_typ.bind('<<ComboboxSelected>>',
                          lambda x: self.fld_typ.selection_clear())

        self.btn_save.configure(command=self._save_person)

    def on_cancel(self) -> None:
        '''Wenn Abbruch gesendet wird'''
        self._on_cancel_btn()

    def _on_cancel_btn(self) -> None:
        if self.person:
            self.controller.personendetails_anzeigen(self.person.id)
        else:
            self.controller.personenliste_anzeigen()

    def show(self, person: Person) -> None:
        '''im Vergleicht zur Standardmethode "tkraise" wird hier die anzuzeigende Person gesetzt und die Anzeige der Personendaten aktualisiert'''
        self.person = person
        self._fill_form()
        self.tkraise()
        self.master.top = self

    def _fill_form(self) -> None:
        '''Fuellt die Datenfelder mit den Personendaten'''

        typen = {'P': 'P - Einzelperson',
                 'G': 'G - Gemeinschaftsperson',
                 'J': 'J - Jur. Person'}

        if self.person:
            self.data['person_id'].set(self.person.id)
            self.data['kdnr'].set(self.person.kdnr)
            self.data['typ'].set(typen[self.person.typ])
            self.data['anrede'].set(
                self.person.anrede) if self.person.anrede else ''
            self.data['titel'].set(
                self.person.titel if self.person.titel else '')
            self.data['nachname'].set(self.person.nachname)
            self.data['vorname'].set(
                self.person.vorname if self.person.vorname else '')
            self.data['geboren'].set(
                date.strftime(self.person.geboren, '%d.%m.%Y') if self.person.geboren else '')
            self.data['verstorben'].set(
                date.strftime(self.person.verstorben, '%d.%m.%Y') if self.person.verstorben else '')
            self.data['post_erg'].set(
                self.person.post_erg if self.person.post_erg else '')
            self.data['strasse'].set(
                self.person.strasse if self.person.strasse else '')
            self.data['plz'].set(self.person.plz if self.person.plz else '')
            self.data['ort'].set(self.person.ort if self.person.ort else '')
            self.data['land'].set(self.person.land if self.person.land else '')
            self.data['tel1'].set(self.person.tel1 if self.person.tel1 else '')
            self.data['tel2'].set(self.person.tel2 if self.person.tel2 else '')
            self.data['email'].set(
                self.person.email if self.person.email else '')
            self.fld_hinweise.delete('1.0', 'end')
            self.fld_hinweise.insert(
                'end', self.person.hinweise if self.person.hinweise else '')
            self.neu_anlegen = False
        else:
            self.data['person_id'].set("")
            self.data['kdnr'].set('')
            self.data['typ'].set('')
            self.data['anrede'].set('')
            self.data['titel'].set('')
            self.data['nachname'].set('')
            self.data['vorname'].set('')
            self.data['geboren'].set('')
            self.data['verstorben'].set('')
            self.data['post_erg'].set('')
            self.data['strasse'].set('')
            self.data['plz'].set('')
            self.data['ort'].set('')
            self.data['land'].set('')
            self.data['tel1'].set('')
            self.data['tel2'].set('')
            self.data['email'].set('')
            self.fld_hinweise.text.delete('1.0', 'end')
            self.neu_anlegen = True

    def _save_person(self) -> None:
        '''Speichert die veränderten Personendaten'''

        try:
            p_save = Person(
                id=int(self.data['person_id'].get()
                       ) if self.data['person_id'].get() else None,
                typ=self.data['typ'].get()[:1],
                anrede=self.data['anrede'].get(),
                titel=self.data['titel'].get(),
                nachname=self.data['nachname'].get(),
                vorname=self.data['vorname'].get(),
                geboren=datetime.strptime(self.data['geboren'].get(), '%d.%m.%Y').date() if len(
                    self.data['geboren'].get()) > 0 else None,
                verstorben=datetime.strptime(self.data['verstorben'].get(), '%d.%m.%Y').date(
                ) if len(self.data['verstorben'].get()) > 0 else None,
                gekuendigt=datetime.strptime(self.data['gekuendigt'].get(), '%d.%m.%Y').date(
                ) if len(self.data['verstorben'].get()) > 0 else None,
                post_erg=self.data['post_erg'].get(),
                strasse=self.data['strasse'].get(),
                plz=self.data['plz'].get(),
                ort=self.data['ort'].get(),
                land=self.data['land'].get(),
                tel1=self.data['tel1'].get(),
                tel2=self.data['tel2'].get(),
                email=self.data['email'].get(),
                kdnr=self.data['kdnr'].get(),
                hinweise=self.fld_hinweise.get('1.0', 'end')[:-1]
            )
            if self.neu_anlegen:
                self.controller.person_anlegen(p_save)
            else:
                self.controller.person_aendern(p_save)
        except ValueError as ve:
            self.controller.nachricht_anzeigen(ve.args)
