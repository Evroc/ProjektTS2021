import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time


#-----------------------slave

color_map = []
color_map_sla = []

cords_sl = {"Obiekt w CNC": (0, 0),
            "Obrobka": (2, 0),
            "Odlozenie": (1, -1)
         }

options_sl = {
    'node_color': color_map_sla,
    'edge_color': 'red',
    'node_size': 800,
    'width': 2,
    'with_labels': True,
    'pos': cords_sl,
    'node_shape': 'D'
}

edges_sl = {
   # ("Zamkniecie drzwi elementu podrzednego", "Odlozenie"),
    ("Obiekt w CNC", "Obrobka"),
    ("Obrobka", "Odlozenie"),
    ("Odlozenie", "Obiekt w CNC")
}

nodes_sl = [
    #"Zamkniecie drzwi elementu podrzednego"
    "Obiekt w CNC", #1
    "Obrobka",#2
    "Odlozenie"#3
]
#----------------- master autom
cords = {"Zamkniecie drzwi elementu podrzednego": (-5, 0),
         "Obiekt w podajniku": (-5, 2),
         "Przenoszenie do CNC": (-3, 2),
         "CNC": (-1, 2),
         "Kontrola jakosci": (1, 2),
         "Element odrzucony": (3, 2),
         #2linia
         "Przeniesienie obiektu do pudelek": (2, 1.5),
         "Odbior": (-1, 1.5),
         "Proces zatrzymany": (-4, 1.5),
         }

options_g = {
    'node_color': color_map,
    'edge_color': 'blue',
    'node_size': 18000,
    'width': 0.5,
    'with_labels': True,
    'pos': cords,
    'node_shape': 's',
    'font_size': 13,

}

edges = [("Obiekt w podajniku", "Przenoszenie do CNC"),
         ("Obiekt w podajniku", "Proces zatrzymany"),
         ("Przenoszenie do CNC", "CNC"),
         ("CNC", "Kontrola jakosci"),
         ("Kontrola jakosci", "Element odrzucony"),
         ("Kontrola jakosci", "Przeniesienie obiektu do pudelek"),
         #("Element odrzucony", "Obiekt w podajniku"),
         ("Przeniesienie obiektu do pudelek", "Odbior"),
         ("Przeniesienie obiektu do pudelek", "Obiekt w podajniku"),
         ("Odbior", "Proces zatrzymany"),
         ("Proces zatrzymany", "Obiekt w podajniku")
         ]

nodes = ["Obiekt w podajniku", #1
         "Przenoszenie do CNC",#2
         "Proces zatrzymany",#3
         "CNC",#4
         "Kontrola jakosci",#5
         "Element odrzucony",#6
         "Przeniesienie obiektu do pudelek",#7
         "Odbior",#8
         ]
#ew todo strzalki
#dodanie x, y wspoł napisow - matplotlib dodanie !
labels = {('Obiekt w podajniku', 'Przenoszenie do CNC'): "Sygnał - Nowy element!",
          ("Obiekt w podajniku", "Proces zatrzymany"): "STOP!",
          ("Przenoszenie do CNC", "CNC"): "Element odłożony!",
          ("CNC", "Kontrola jakosci"): "Element gotowy!",
          ("Kontrola jakosci", "Element odrzucony"): "Odrzucono!", ("Kontrola jakosci", "Przeniesienie obiektu do pudelek"): "Przyjęto!",
          ("Przeniesienie obiektu do pudelek", "Odbior"): "Pudełko pełne!", ("Przeniesienie obiektu do pudelek", "Obiekt w podajniku"): "Gotowe!",
          ("Odbior", "Proces zatrzymany"): "Zatrzymanie procesu!",
          ("Proces zatrzymany", "Obiekt w podajniku"): "Wznów!"
         }

g = nx.DiGraph() #master g
h = nx.DiGraph() #slave g
#Addinng edges/nodes master - slave
g.add_edges_from(edges)
g.add_nodes_from(nodes)

h.add_edges_from(edges_sl)
h.add_nodes_from(nodes_sl)

#plt.figure('Slave automa', figsize=(6, 3))
#nx.draw(h, **options_sl)

#plt.draw()
#plt.show()
#plt.figure('Slave automa', figsize=(6, 3))



def draw_graph_slave(current_state):
    plt.ion()

    plt.figure('Slave automa', figsize=(6, 3))
    for node in h:
        if node == current_state:
            color_map_sla.append('blue')
        else:
            color_map_sla.append('red')

    nx.draw(h, **options_sl)
    #plt.draw()
    plt.show()
    color_map_sla.clear()
    plt.pause(1)


def draw_graph(current_state):
    plt.ion()
    plt.figure('Master automa', figsize=(14, 6))
    for node in g:
        if node == current_state:
            color_map.append('blue')
        else:
            color_map.append('red')
    nx.draw(g, **options_g)
    plt.show()
    color_map.clear()
    plt.pause(1)
