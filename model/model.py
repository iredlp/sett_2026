import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMapA = {}

    def creaGrafo(self, v_min, v_max):
        self._grafo.clear()
        self._idMapA.clear()
        actors = DAO.getAllNodes(v_min, v_max)
        for a in actors:
            self._idMapA[a.id] = a
            self._grafo.add_node(a)

        movies = DAO.getFilmPerAttore(v_min, v_max)
        for row in movies:
            actor = self._idMapA[row[0]]
            actor.movies.append(
                (row[1], row[2], row[3], row[4]) )

            #SE NON AVESSI USATO LE TUPLE, MA SOLO ROW NEL DAO
           # actor = self._idMapA[row["name_id"]] #recupero dall'idMap
           # actor.movies.append(
             #   (row["title"], row["year"], row["avg_rating"]))

        for i in range(len(actors)):
            for j in range(i + 1, len(actors)):
                a1 = actors[i]
                a2 = actors[j]

                #creo un set per a1 e un set per a2
                films1 = set()
                for film in a1.movies:
                    films1.add(film[0])

                films2 = set()
                for film in a2.movies:
                    films2.add(film[0])

                comuni = films1 & films2

                # Calcolo del peso secondo la traccia
                peso = len(comuni)
                if peso > 0:
                    self._grafo.add_edge(a1, a2, weight=peso)

                #OPPIRE CON LA LISTA- ma meno efficente
                #comuni = []
              #  for film1 in a1.movies:
                #    for film2 in a2.movies:
                     #   if film1[0] == film2[0]:
                        #    comuni.append(film1[0])
               # peso = len(comuni)
        for actor in self._grafo.nodes:
            if self._grafo.degree(actor) == 14:
                print(actor.name)

    def getAllNodes(self,  v_min, v_max):
        return DAO.getAllNodes(v_min, v_max)


    def get_num_nodes(self) -> int:
        return self._grafo.number_of_nodes()

    def get_num_edges(self) -> int:
        return self._grafo.number_of_edges()

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

     #GRADO MAX
    def getActorMaxDegree(self):
        return max( self._grafo.nodes,  key=lambda a:(  -self._grafo.degree(a), a.name ))

    #5 ARCHI DI PESO MAGGIORE- in ordine DEC ma in caso di parità considera ordine alfabetico
    def getTop5Archi(self):
        return sorted(self._grafo.edges(data=True), key=lambda x: (-x[2]["weight"], x[0].name, x[1].name))[:5]

    def getSumPesiArchiMax(self):
        # Lista di tuple: (Prodotto, score)
        classifica = []

        for nodo in self._grafo.nodes:
            # Somma dei pesi degli archi
            peso = sum(d["weight"] for u, v, d in self._grafo.in_edges(nodo, data=True))

            peso += sum(
                d["weight"]
                for u, v, d in self._grafo.out_edges(nodo, data=True)
            )

            classifica.append((nodo, peso))

        # Ordiniamo in ordine decrescente di score
        classifica.sort(key=lambda x: x[1], reverse=True)

        return classifica[0]

    #attore più giovane
    def getYoungestActor(self):
        actors = [a for a in self._grafo.nodes if a.date_of_birth is not None]
        return max(actors, key=lambda a: a.date_of_birth)

    #attore più vecchio
    def getOldestActor(self):
        actors = [a for a in self._grafo.nodes if a.date_of_birth is not None]
        return min(actors, key=lambda a: a.date_of_birth)



    #RICORSIONEEE
    def getGruppoAttori(self, start_node, k):
        self._best_path = []
        self._best_score = -1

        # Il percorso parziale parte con il nodo selezionato
        parziale = [start_node]
        self._ricorsione(parziale, k)

        return self._best_path, self._best_score

    def _ricorsione(self,parziale, k):

        if len(parziale) == k:
            score = sum(len(a.movies) for a in parziale)

            if score > self._best_score:
                self._best_score = score
                self._best_group = list(parziale)

            return
        candidati = set()

        for actor in parziale:
            candidati.update(self._grafo.successors(actor))
            candidati.update(self._grafo.predecessors(actor))

        # provo solo i candidati adiacenti a qualcuno del gruppo
        for candidato in candidati:

            if candidato in parziale:
                continue

            # conto quanti attori già nel gruppo sono adiacenti
            contatti = 0

            for actor in parziale:
                if (self._grafo.has_edge(actor, candidato) or
                        self._grafo.has_edge(candidato, actor)):
                    contatti += 1

                #for attore in parziale:
               # if (self._grafo.has_edge(attore, candidato) or
                      #  self._grafo.has_edge(candidato, attore)):
                    #contatti += 1

            # deve essere collegato ad ESATTAMENTE UN attore
            if contatti == 1:
                parziale.append(candidato)
                # Chiamata ricorsiva passando il nuovo arco come riferimento
                self._ricorsione(parziale, k)
                # BACKTRACKING: annullo l'ultima mossa
                parziale.pop()



    def _score(self, parziale):
        #esplora la soluz parzila ed aggiunge i pesi
        score=0
        for actor in parziale:
            score+=len(actor.movies)
        return score


