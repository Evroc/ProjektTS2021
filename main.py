from generator import Generator
from statemachine import StateMachine, State, Transition
from tranzycja import *


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


# create a supervisor
supervisor = Generator.create_master(master_states, master_transitions)




# run supervisor for exemplary path
#print("--------------------------")

#print(f"Jesteś w punkcie {supervisor.current_state}")

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
#print(supervisor.current_state[1])
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



#print(f"2Jesteś w punkcie {supervisor.current_state}")

#print("Executing path: {}".format(paths))

#abc = input(f"Jestes w:  {supervisor.current_state.value}")



#n = input(f"Znajdujesz się w {supervisor.current_state.value}, wybierz 1 żeby przenieść obiekt do CNC lub 2 żeby zatrzymać proces ")
# launch a transition in our supervisor
print("-------------------")
print("Nastapilo wyjscie z programu")
print("-------------------")

