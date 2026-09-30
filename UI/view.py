import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP - Esame del 14 Settembre 2026 - Traccia A"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._txt_result = None

        self._txtRatingMin = None
        self._txtRatingMax = None
        self._btnCreaGrafo = None
        self._btnStampaInfo = None

        self._ddActor = None
        self._txtInN = None
        self._btnTrovaGruppo = None

    def load_interface(self):
        # title
        self._title = ft.Text("TdP - Esame del 14 Settembre 2026 - Traccia A", color="blue", size=24)
        self._page.controls.append(self._title)

        # riga 1
        self._txtRatingMin = ft.TextField(label="Valutazione minima", value="7.0")
        self._txtRatingMax = ft.TextField(label="Valutazione massima", value="10.0")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea grafo",
                                                on_click=self._controller.handleCreaGrafo)
        self._btnStampaInfo = ft.ElevatedButton(text="Stampa Info",
                                                 on_click=self._controller.handleStampaInfo)

        row1 = ft.Row([ft.Container(self._txtRatingMin, width=180),
                       ft.Container(self._txtRatingMax, width=180),
                       ft.Container(self._btnCreaGrafo, width=180),
                       ft.Container(self._btnStampaInfo, width=180)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # riga 2
        self._ddActor = ft.Dropdown(label="Attore")
        self._txtInN = ft.TextField(label="Numero di attori (N)")
        self._btnTrovaGruppo = ft.ElevatedButton(text="Trova gruppo attori",
                                                  on_click=self._controller.handleTrovaGruppo)
        self._controller.fillDDAttori()

        row2 = ft.Row([ft.Container(self._ddActor, width=300),
                       ft.Container(self._txtInN, width=150),
                       ft.Container(self._btnTrovaGruppo, width=220)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # List View for output print
        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self._txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
