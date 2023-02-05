import ttkbootstrap as ttb

from model.controller import Controller


class ButtonBar(ttb.Frame):
    '''Die Buttonleiste im Hauptfenster'''

    def __init__(self, master, controller: Controller):
        super().__init__(master=master)

        self.controller: Controller = controller

        self._build_ui()
        self._register_bindings()

    def _build_ui(self):
        self.btn_personenliste = ttb.Button(
            self, text="Personenliste anzeigen")
        self.btn_personenliste.pack(side='top', fill='x', padx=10, pady=10)

        self.btn_person_neu = ttb.Button(self, text='Neue Person anlegen')
        self.btn_person_neu.pack(side='top', fill='x', padx=10, pady=10)

        self.btn_buchungsmaske = ttb.Button(self, text='Buchungen durchführen')
        self.btn_buchungsmaske.pack(side='top', fill='x', padx=10, pady=10)

    def _register_bindings(self) -> None:
        self.btn_personenliste.configure(
            command=lambda: self.controller.personenliste_anzeigen())

        self.btn_person_neu.configure(
            command=lambda: self.controller.person_aendern_bildschirm_anzeigen())

        self.btn_buchungsmaske.configure(
            command=lambda: self.controller.buchungsmaske_anzeigen())
