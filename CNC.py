from statemachine import State, Transition
from tranzycja import *

options_cnc = [
    {"name": "Obiekt w CNC", "initial": True, "value": "obiekt_w_cnc"}, #0
    {"name": "Obróbka", "initial": False, "value": "obrobka"}, #1
    {"name": "Odlozenie gotowego elementu", "initial": False, "value": "odlozenie_gotowego elementu"}, #2

]

states = [State(**opt) for opt in options_cnc]

# valid transitions for a master (indices of states from-to)
form = [
    [0, [1]],
    [1, [2]],
    [2, [3]],
]

master_states_cnc, master_transitions_cnc = setTransition(form, states, 'cnc')

przejscie_cnc = ["cnc_0_1", "cnc_1_2", "cnc_2_3"] #jedno mozliwe przejscie
