import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()
        n_min=float(self._view._txtRatingMin.value)
        n_max=float(self._view._txtRatingMax.value)

        if not n_min:
            self._view.create_alert("Selezionare un valore minimo prima di creare il grafo.")
            return
        if not n_max:
            self._view.create_alert("Selezionare un valore massimo prima di creare il grafo.")
            return
        try:
            self._model.creaGrafo(n_min, n_max)
            n_nodes = self._model.get_num_nodes()
            n_edges = self._model.get_num_edges()

            # Stampa immediata numero di vertici e archi (Punto 1.c)
            self._view._txt_result.controls.append(
                ft.Text(f"Grafo creato con successo!\nNumero vertici: {n_nodes}\nNumero archi: {n_edges}") )

        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore durante la creazione del grafo: {ex}", color="red")
            )
        self._view.update_page()


    def handleStampaInfo(self, e):
        # Verifica preventiva che il grafo sia stato creato
        if self._model.get_num_nodes() == 0 or self._model.get_num_edges() is None:
            self._view.create_alert("Creare prima il grafo!",  color="red")
            return

        #ATTORE CON GRADO MAX
        actor_degree = self._model.getActorMaxDegree()
        self._view._txt_result.controls.append(
            ft.Text( f"Attore con grado maggiore: {actor_degree.name} "
                      f"(grado: {self._model._grafo.degree(actor_degree)})") )

        # Attore con somma dei pesi maggiore
        actor_weight, peso = self._model.getSumPesiArchiMax()
        self._view._txt_result.controls.append(
            ft.Text(
                f"Attore con somma pesi maggiore: {actor_weight.name} "
                f"(somma pesi: {peso})"
            )
        )

        top5 = self._model.getTop5Archi()
        self._view._txt_result.controls.append(ft.Text(f"Archi di peso maggiore", color="green"))
        for arco in top5:
            self._view._txt_result.controls.append(ft.Text(f"{arco[0]}-->{arco[1]} (peso: {arco[2]["weight"]})"))

        self._view._txt_result.controls.append(ft.Text(" "))

        #  Attore più giovane
        youngest = self._model.getYoungestActor()
        self._view._txt_result.controls.append(
            ft.Text(f"Attore più giovane: {youngest.name} "
                f"({youngest.date_of_birth})" ) )

        #  Attore più anziano
        oldest = self._model.getOldestActor()
        self._view._txt_result.controls.append(
            ft.Text(f"Attore più anziano: {oldest.name} "f"({oldest.date_of_birth})"))

        self._view.update_page()

    def fillDDAttori(self):
        n_min = float(self._view._txtRatingMin.value)
        n_max = float(self._view._txtRatingMax.value)

        if not n_min:
            self._view.create_alert("Selezionare un valore minimo prima di creare il grafo.")
            return
        if not n_max:
            self._view.create_alert("Selezionare un valore massimo prima di creare il grafo.")
            return
        attori = self._model.getAllNodes(n_min, n_max)
        for actor in attori:
            self._view._ddActor.options.append(ft.dropdown.Option(
                key=actor.id,
                text=actor.name))

        self._view.update_page()

    def handleTrovaGruppo(self, e):
        self._view._txt_result.controls.clear()

        k = self._view._txtInN.value
        # qui dovremmo fare i solti controlli sulla validità

        try:
             kInt=int(k)
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore ! devi inserire un intero per procedere: {ex}", color="red")
            )
            self._view.update_page()
            return

       # kInt=int(k)
        # recupero l'attore selezionato dal Dropdown
        start_node = self._model._idMapA[self._view._ddActor.value]

        if self._view._ddActor.value is None:
            self._view.create_alert("Selezionare prima un attore di partenza.", color="red")
            return

        listAttori, bestScore = self._model.getGruppoAttori( start_node,kInt)

        if listAttori is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(
                f"Non ci sono abbastanza comoonenti connesse per trovare N ATTORI", color="red"))
            return
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(
            f" Di seguito il Gruppo di N Attori ADIACENTI, massimizzando il numero di film:", color="green"))
        for p in listAttori:
            self._view._txt_result.controls.append(ft.Text(p))
        self._view.update_page()

