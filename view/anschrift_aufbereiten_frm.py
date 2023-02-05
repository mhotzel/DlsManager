from ttkbootstrap import Toplevel
from model.controller import Controller

from model.person import Person


class AnschriftAufbereitenFrm(Toplevel):

    def __init__(self, master, person: Person, controller: Controller):
        super().__init__(title='Anschrift aufbereiten', master=master)
        self.controller = controller
        self.person = person

    def _build_ui(self):
        self.transient(self.master)

        self.position_center()
        self.wait_visibility()

        self.grab_set()
        self.wait_window()

    def ausblenden(self) -> None:
        self.grab_release()
        self.destroy()
