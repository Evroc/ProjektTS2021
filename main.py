from statemachine import StateMachine, State, Transition

import keyboard
import msvcrt as m

class MachineClass(StateMachine):
    #states
    object_in = State('start', initial=True)
    move_object = State('Move objects to cnc')
    cnc = State('cnc')
    quality_control = State('Quality control')
    move_final_objects = State('Move objects to boxes')
    objects_receive = State('Receive objects in the boxes')
    hold = State('Process stopped')

    #transitions???????????????????????? whats that
    signal = object_in.to(move_object)
    object_left = move_object.to(cnc)
    object_ready = cnc.to(quality_control)
    ok = quality_control.to(move_final_objects)
    box_isFull = move_final_objects.to(objects_receive)
    something = objects_receive.to(hold)
    restart = hold.to(object_in)

    #queue = [object_in, move_object, cnc]
    #list =[signal, object_left, object_ready]

    #def please(self, state):
    #    for in

    def on_signal(self):
        print('Signal received!')

    def on_object_left(self):
        print('Object left!')

def wait():
    m.getch()

#list = [MachineClass.signal, MachineClass.object_left, MachineClass.object_ready, MachineClass.ok]

abc = MachineClass()

#tests

print('------------------')
print(abc.is_object_in)
print(abc.is_move_object)
print(abc.is_cnc)
print('------------------')
abc.signal()
print('------------------')
print(abc.is_object_in)
print(abc.is_move_object)
print(abc.is_cnc)
print('------------------')
abc.object_left()
print('------------------')
print(abc.is_object_in)
print(abc.is_move_object)
print(abc.is_cnc)
print('------------------')


