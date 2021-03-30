from generator import Generator
from statemachine import StateMachine, State, Transition
from tranzycja import *
import networkx as nx
import matplotlib.pyplot as plt

# define states for a master (way of passing args to class)

options = [
    {"name": "Obiekt w podajniku", "initial": True, "value": "obiekt_w_podajniku"}, #0
    {"name": "Przenoszenie do CNC", "initial": False, "value": "przenoszenie_do_cnc"}, #1
    {"name": "CNC", "initial": False, "value": "cnc"}, #2
    {"name": "Kontrola jakości", "initial": False, "value": "kontrola_jakosci"}, #3
    {"name": "Element odrzucony", "initial": False, "value": "element_odrzucony"}, #4
    {"name": "Przeniesienie obiektu do pudelek", "initial": False, "value": "przeniesienie_obiektu_do_pudelek"}, #5
    {"name": "Odbior", "initial": False, "value": "odbior"}, #6
    {"name": "Proces zatrzymany", "initial": False, "value": "proces_zatrzymany"}, #7

]


# create State objects for a master
# ** -> unpack dict to args
master_states = [State(**opt) for opt in options]

# valid transitions for a master (indices of states from-to)
from_to = [
    [0, [1, 7]],
    [1, [2]],
    [2, [3]],
    [3, [4, 5]],
    [4, [0]],
    [5, [6, 0]],
    [6, [7]],
    [7, [0]],
]



master_states, master_transitions = setTransition(from_to, master_states, 'r')
#master_transitions = {}



# create paths from transitions (exemplary)
path_1 = ["0_1", "1_2", "2_3", "3_5", "5_0"] #bez odrzucenia kontrolii jakosci i bez przepelnionego pudelka
path_2 = ["0_1", "1_2", "2_3", "3_4", "4_6", "6_0"]
path_3 = ["0_1", "1_2", "2_3", "3_0"]
paths = [path_1]

# execute paths
#GRAF!!!
G = nx.petersen_graph()
elist = [("Obiekt w podajniku", "Przenoszenie do CNC"), ("Obiekt w podajniku", "Proces zatrzymany"),
         ("Przenoszenie do CNC", "CNC"),
         ("CNC", "Kontrola jakości"),
         ("Kontrola jakości", "Element odrzucony"), ("Kontrola jakości", "Przeniesienie obiektu do pudelek"),
         ("Element odrzucony", "Obiekt w podajniku"),
         ("Przeniesienie obiektu do pudelek", "Odbior"), ("Przeniesienie obiektu do pudelek", "Obiekt w podajniku"),
         ("Odbior", "Proces zatrzymany"),
         ("Proces zatrzymany", "Obiekt w podajniku")
         ]
llist = {("Obiekt w podajniku", "Przenoszenie do CNC"): "Sygnał - Nowy element!",
         ("Obiekt w podajniku", "Proces zatrzymany"): "STOP!",
         ("Przenoszenie do CNC", "CNC"): "Element odłożony!",
         ("CNC", "Kontrola jakości"): "Element gotowy!",
         ("Kontrola jakości", "Element odrzucony"): "Odrzucono!", ("Kontrola jakości", "Przeniesienie obiektu do pudelek"): "Przyjęto!",
         ("Element odrzucony", "Obiekt w podajniku"): "Nowy element!",
         ("Przeniesienie obiektu do pudelek", "Odbior"): "Pudełko pełne!", ("Przeniesienie obiektu do pudelek", "Obiekt w podajniku"): "Gotowe!",
         ("Odbior", "Proces zatrzymany"): "Zatrzymanie procesu!",
         ("Proces zatrzymany", "Obiekt w podajniku"): "Wznów!"
         }

G.add_edges_from(elist)

#nx.draw_circular(G, **llist)
#do tego wyzej nazwy w ''
#nx.draw_shell(G, nlist=[range(5, 10), range(5)], llist, font_weight='bold')

val_map = {'Obiekt w podajniku': 1.0,
           'CNC': 1.0,
           'Odbior': 1.0}

values = [val_map.get(node, 0.5) for node in G.nodes()]

red_edges = [('Obiekt w podajniku', 'Przenoszenie do CNC')]
edge_colours = ['black' if not edge in red_edges else 'red'
                for edge in G.edges()]
black_edges = [edge for edge in G.edges() if edge not in red_edges]

# Need to create a layout when doing
# separate calls to draw nodes and edges
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
                       node_color = values, node_size = 500)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
plt.show()


# create a supervisor
supervisor = Generator.create_master(master_states, master_transitions)


#debugowanie glownej logiki
# for i in enumerate(from_to):
#     try:
#         print(i)
#
#     except:
#         print("error_msg")
# print(from_to[0][1][0])

print("********START************")
print("Jestes w stanie startowym: ")
print(supervisor.current_state.name)
print("--------------------------")
print("Aby dokonac przejscia podaj wartosc z ktorej tranzycji_do ktorej tranzycji, aby wyjsc wpisz quit")
print("Twoje obecne mozliwe tranzycje to:")
for t in from_to[0][1]:
    too_long = master_transitions[f'0_{t}'].identifier
    if too_long == "0_1":
        print(too_long, " - Otrzymano sygnal o nowym elemencie")
    if too_long == "0_7":
        print(too_long, " - Zatrzymanie procesu")

while 1:
    print("-------------------")
    x = input("Wpisz wybrana tranzycje: ")
    if x == str('quit'):

        break

    master_transitions[x]._run(supervisor)
    print("-------------------")
    print("Twoj obecny stan to: ", supervisor.current_state.name)
    print("Obecne mozliwe tranzycje to: ")
    for t in from_to[int(x[2])][1]:
        too_long = master_transitions[f"{int(x[2])}_{t}"].identifier
        #print(master_transitions[f"{int(x[2])}_{t}"].identifier)
        if too_long == "0_1":
            print(too_long, " - Otrzymano sygnal o nowym elemencie")
        if too_long == "0_7":
            print(too_long, " - Zatrzymanie procesu")
        if too_long == "1_2":
            print(too_long, " - Odlozenie elementu")
        if too_long == "2_3":
            print(too_long, " - Element do kontroli jakosci")
        if too_long == "3_4":
            print(too_long, " - Element ma wade - odrzuc")
        if too_long == "3_5":
            print(too_long, " - Element bez wad - przyjmij")
        if too_long == "4_0":
            print(too_long, " - Element odrzucony - powrot do poczatku")
        if too_long == "5_0":
            print(too_long, " - Potrzebuje wiecej elementow w pudelku!")
        if too_long == "5_6":
            print(too_long, " - Mam wystarczajaco elementow w pudelku!")
        if too_long == "6_7":
            print(too_long, " - Odebrano elementy, wstrzymaj proces")
        if too_long == "7_0":
            print(too_long, " - Wznowienie procesu")

print("-------------------")
print("Nastapilo wyjscie z programu")
print("-------------------")

