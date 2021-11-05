import numpy as np
import matplotlib.pyplot as plt
import math

w0 = 18.0822
beta = 0.0699

K = math.exp((-beta*math.pi)/(math.sqrt(1-beta**2)))
delta_T = math.pi/(w0*math.sqrt(1-beta**2))
D = 1 + 3*K + 3*(K**2) + math.pow(K,3)

shape_stages = np.array([1/D,
                        3*K/D,
                        3*(K**2)/D,
                        math.pow(K,3)/D])

shape_input_start_time = 0
stage = 0
def shape_input(curr_vel, set_vel, accel, curr_time):
    global shape_input_start_time
    global stage

    if accel == 1 and stage < 4:
        del_vel = shape_stages[stage] * set_vel
    elif accel == -1 and stage < 4:
        del_vel = -shape_stages[stage] * set_vel

    if curr_time > shape_input_start_time and curr_time < shape_input_start_time + delta_T and stage == 0: # first stage
        curr_vel += del_vel
        stage = 1
    elif curr_time > shape_input_start_time + delta_T and curr_time < shape_input_start_time + 2*delta_T and stage == 1: # second stage
        curr_vel += del_vel
        stage = 2
    elif curr_time > shape_input_start_time + 2*delta_T and curr_time < shape_input_start_time + 3*delta_T and stage == 2: # third stage
        curr_vel += del_vel
        stage = 3
    elif curr_time > shape_input_start_time + 3*delta_T and stage == 3: # final stage
        curr_vel += del_vel
        stage = 4
    
    return curr_vel

if __name__ == '__main__':
    # global shape_input_start_time
    dt = 0.001

    start_time = 0
    curr_time = start_time

    curr_vel = 0
    set_vel = 225
    v = []
    t = []

    change = 1
    accel = 0

    #input shaping loop
    while(curr_time < start_time+2):
        if curr_time > 0 and change==1:
            accel = 1
            stage = 0
            shape_input_start_time = curr_time
            change = 2
        elif curr_time > 0.6 and change == 2:
            accel = -1
            stage = 0
            shape_input_start_time = curr_time
            change = 3
        
        if change >= 2:
            curr_vel = shape_input(curr_vel, set_vel, accel, curr_time)

        v.append(curr_vel)
        t.append(curr_time)
        curr_time += dt

    plt.plot(v, label='input_shapping')
    # plt.show()



    # normal loop
    start_time = 0
    curr_time = start_time
    v = []
    vel = 0
    while(curr_time < start_time+2):
        if curr_time > 1.123:
            vel = 0
        elif curr_time > 0:
            vel = set_vel
        v.append(vel)
        t.append(curr_time)
        curr_time += dt

    plt.title('Simulation of step input and input shaping')
    plt.ylabel('vel (deg/s)')
    plt.xlabel('time (ms)')
    plt.plot(v, label='step_input')
    plt.legend()
    plt.show()