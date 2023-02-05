from os.path import join

from ttkbootstrap import Label, Separator, Window

from model.config import RES_DIR
from model.controller import Controller
from view.anschrift_aufbereiten_frm import AnschriftAufbereitenFrm
from view.buchungsmaske_frm import BuchungsmaskeFrm
from view.button_bar import ButtonBar
from view.konto_aendern_frm import KontoAendernFrm
from view.konto_anlegen_frm import KontoAnlegenFrm
from view.kontouebersicht_frm import KontouebersichtFrm
from view.person_aendern_frm import PersonAendernFrame
from view.personendetails_frm import PersonenDetailsFrame
from view.personenliste_frm import PersonenListeFrame


class MainWindow(Window):

    def __init__(self, controller: Controller):
        super().__init__(title="DLS Manager", themename='yeti',
                         iconphoto=join(RES_DIR, 'img', 'logo.png'))
        self.controller: Controller = controller

        self._build_ui()
        self.position_center()
        self._register_bindings()

    def _build_ui(self):

        self._frames = {
            PersonenListeFrame: PersonenListeFrame(self, self.controller),
            PersonenDetailsFrame: PersonenDetailsFrame(self, self.controller),
            PersonAendernFrame: PersonAendernFrame(self, self.controller),
            KontouebersichtFrm: KontouebersichtFrm(self, self.controller),
            KontoAnlegenFrm: KontoAnlegenFrm(self, self.controller),
            BuchungsmaskeFrm: BuchungsmaskeFrm(self, self.controller)
        }

        for k, f in self._frames.items():
            f.grid(column=2, row=0, sticky='NSEW')

        self._frames[PersonenListeFrame].show()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        self.buttonbar = ButtonBar(self, self.controller)
        self.buttonbar.grid(column=0, row=0, sticky='NSW', padx=10, pady=10)

        self.buttonbar_sep = Separator(self, orient='vertical')
        self.buttonbar_sep.grid(column=1, row=0, sticky='NS')

        self.status_sep = Separator(self, orient='horizontal')
        self.status_sep.grid(column=0, row=1, columnspan=3, sticky='WE')

        self.status_bar = Label(
            self, font=('', '10', 'bold'))
        self.status_bar.grid(column=0, row=2, columnspan=3,
                             sticky='SWE', padx=5, pady=5)

    def _register_bindings(self) -> None:
        '''Bindet die Elemente, um auf Events zu reagieren'''

        self.controller.register(
            self.controller.EVT_PERSONENDETAILS_ANZEIGEN, lambda person, kontenliste: self._frames[PersonenDetailsFrame].show(person, kontenliste))

        self.controller.register(
            self.controller.EVT_PERSON_AENDERN, lambda person: self._frames[PersonAendernFrame].show(person))

        self.controller.register(
            self.controller.EVT_PERSONENLISTE_ANZEIGEN, lambda: self._frames[PersonenListeFrame].show(
            )
        )

        self.controller.register(
            self.controller.EVT_KONTOUEBERSICHT_ANZEIGEN, lambda kto, umsaetze: self._frames[KontouebersichtFrm].show(
                kto, umsaetze)
        )

        self.controller.register(
            self.controller.EVT_NACHRICHT, lambda msg: self.set_status_message(
                msg, 10000)
        )

        self.controller.register(self.controller.EVT_KONTO_ANLEGEN_ANZEIGEN, lambda person,
                                 produktauswahl: self._frames[KontoAnlegenFrm].show(person, produktauswahl))

        self.controller.register(self.controller.EVT_BUCHUNGSMASKE_ANZEIGEN,
                                 lambda: self._frames[BuchungsmaskeFrm].show())

        self.controller.register(self.controller.EVT_KONTO_AENDERN_ANZEIGEN,
                                 lambda konto: KontoAendernFrm(self, konto, self.controller))

        self.controller.register(self.controller.EVT_ANSCHRIFT_AUFBEREITEN_ANZEIGEN,
                                 lambda person: AnschriftAufbereitenFrm(self, person, self.controller))

        self.bind_all('<KeyPress-Escape>', lambda e: self.controller.personenliste_anzeigen())

        self.bind_all('<Control-f>', lambda e: self.controller.personenliste_anzeigen())

    def set_status_message(self, text: str, millis: int = 0):
        '''Zeigt eine Statusnachricht unten im Hauptfenster an'''
        self.status_bar.configure(text=text)
        if millis > 0:
            self.after(millis, lambda: self.status_bar.configure(text=''))

