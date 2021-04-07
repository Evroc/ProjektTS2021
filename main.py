from generator import Generator
from statemachine import StateMachine, State, Transition
from tranzycja import *
from nx import *
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
    {"name": "Proces zatrzymany", "initial": False, "value": "proces_zatrzymany"} #7

]


options_slave = [
    {"name": "Obiekt w CNC", "initial": True, "value": "obiekt_w_cnc"},  # 0
    {"name": "Obrobka", "initial": False, "value": "obrobka"},  # 1
    {"name": "Odlozenie", "initial": False, "value": "odlozenie"}  # 2
]

# create State objects for a master
# ** -> unpack dict to args
master_states = [State(**opt) for opt in options]
slave_states = [State(**opt) for opt in options_slave]

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

from_to_slave = [
    [0, [1]],
    [1, [2]],
    [2, [0]],
]

slave_states, slave_transitions = setTransition(from_to_slave, slave_states, 's')
master_states, master_transitions = setTransition(from_to, master_states, 'r')


# create a supervisor
supervisor = Generator.create_master(master_states, master_transitions)
slave = Generator.create_master(slave_states, slave_transitions)

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
    print("czesc")
    if x == str('quit'):

        break

    master_transitions[x]._run(supervisor)
    print("-------------------")
    print("Twoj obecny stan to: ", supervisor.current_state.name)

    draw_graph(supervisor.current_state.name)

    print("Obecne mozliwe tranzycje to: ")
    for t in from_to[int(x[2])][1]:
        too_long = master_transitions[f"{int(x[2])}_{t}"].identifier
        state_now = supervisor.current_state.name

        if state_now == "CNC":
            while True:
                if slave.current_state._initial == True:
                    print("0_1 - Zamknięcie drzwi elementu podrzednego")
                a = input("Wpisz wybrana tranzycje: ")
                if a == "2_0":
                    break
                slave_transitions[a]._run(slave)
                print("-------------------")
                print("Twoj obecny stan to: ", slave.current_state.name)
                print("Obecne mozliwe tranzycje to: ")

                for y in from_to_slave[int(a[2])][1]:
                    s_too_long = slave_transitions[f"{int(a[2])}_{y}"].identifier
                    if s_too_long == "0_1":
                        print(s_too_long, " - Zamknięcie drzwi")
                    if s_too_long == "1_2":
                        print(s_too_long, " - Obróbka")
                    if s_too_long == "2_0":
                        print(s_too_long, " - Odłożenie gotowego elementu i powrot do procesu nadrzednego")


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

