from statemachine import State, Transition
from tranzycja import *

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

states = [State(**opt) for opt in options]

# valid transitions for a master (indices of states from-to)
form = [
    [0, [1, 7]],
    [1, [2]],
    [2, [3]],
    [3, [4, 5]],
    [4, [0]],
    [5, [6, 0]],
    [6, [7]],
    [7, [0]],
]

master_states, master_transitions = setTransition(form, states, 'r')

przejscie = ["r_0_1", "r_1_2", "r_2_3", "r_3_5", "r_5_0"] #bez odrzucenia kontrolii jakosci i bez przepelnionego pudelka
przejscie_z_przepelnieniem = ["r_0_1", "r_1_2", "r_2_3", "r_3_4", "r_4_6", "r_6_0"]
przejscie_z_odrzuceniem = ["r_0_1", "r_1_2", "r_2_3", "r_3_0"]