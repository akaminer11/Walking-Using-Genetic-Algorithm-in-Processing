"""
Handles running the actual algorithm to evolve the list of individuals. Also handles whether or not things will be run graphically and slowly or quickly without graphics.
\nMain function is run_generation()
"""

import recombination, selection, creatureFiles
from random import randint
import time

PERCENT_ELITES = 10.0
TIME = 30
TOTAL_FRAMES = TIME * 60
GEN_SIZE = 10

generations = []
# This would be a list of generations. Every time a new generation happens, you would append it to this list.

def generation0(gen_size): # DONE
    l = []
    for i in range(gen_size):
        l.append(creatureFiles.generateOrganism())
    return l


def random(num): # DONE
    """
    Returns a random int from 0 to the entered num (inclusive)
    """
    return randint(0,num)


def run_generation(l): # DONE
    """
    Takes the list of individuals that survived the last culling and their offspring. Returns the list of individuals that survived and their offspring. 
    Runs the actual generation. Can choose to either run things graphically at certain speeds or without graphics instantly*
    \n\n*: As fast as the computer can go.
    """
    MODE = "instant"

    # choose whether to run each individual as graphical at regular speed, fast speed, or instantly
    '''for individual_index in range(len(l)):
        if MODE == "graphically_normal":
            l[individual_index] = run_simulation_graphically(60, 30, l[individual_index], dt, gravity, ground, ground_resolution)
        elif MODE == "graphically_fast":
            l[individual_index] = run_simulation_graphically(600, 5, l[individual_index], dt, gravity, ground, ground_resolution)
        elif MODE == "instant":
            # run the whole generation and leave the loop
            return run_simulation_nongraphically(l, dt, ground, ground_resolution, total_frames, gravity)'''

    # sorts the list based on fitness and culls based on that
    amount = 2*len(l)/4
    new_list = selection.sort_by_fitness(l)
    new_list = new_list[:amount]
    
    newer_list = []
    for i in new_list:
        newer_list.append(i.returnCopy())
        newer_list.append(i.returnCopy())
    
    # calculates the number of individuals to replace the culled individuals and the number of elites
    num_to_be_added = len(l) - len(new_list)
    num_elites = len(l) * PERCENT_ELITES / 100

    # returns the new, filled in list
    return recombination.mutate_everythigng(newer_list)
    
    # return recombination.mate_list(new_list, num_elites, num_to_be_added)


def run_simulation_graphically(framerate, total_time, individual, dt, timer, gravity, ground, ground_resolution, screenTranslate): # SKETCHY BUT PROBABLY DONE
    """
    Runs the simulation graphically. Very sketchy function. In theory, finds the total frames, and, while the frames are less than the total frames,
    updates the simulation at the framerate.
    """
    total_frames = total_time * framerate
    frames = 0
    while frames < total_frames:
        creatureFiles.simulate([individual], ground, gravity, dt, timer, ground_resolution, screenTranslate)
        time.sleep(1.0/framerate)
        background(255)
        frames += 1

    # Find the average x-value of the nodes.
    x_val = 0
    num_nodes = 0
    for i in individual.muscles:
        for x in i.nodes:
           x_val += x.xy[0]
           num_nodes += 1
    
    avg_x_val = x_val/num_nodes

    # updates the individual's fitness
    individual.fitness = avg_x_val
    return individual


def run_simulation_nongraphically(l, dt, ground, ground_resolution, total_frames, gravity): # DONE
    """
    Goes through a list of organisms and updates their fitness to the average x value.
    """
    for i_index in range(len(l)):
        l[i_index].fitness = run_single_nongraphically(l[i_index], ground, ground_resolution, total_frames, dt, gravity)

    return l
    

def run_single_nongraphically(organism, ground, ground_resolution, total_frames, dt, gravity): # DONE
    """
    Runs a single organism and returns the average x value.
    """
    frames = 0
    while frames < total_frames:
        organism.update(dt, frames, gravity, ground, ground_resolution)
        frames += 1

    # Find the average x-value of the nodes.
    x_val = 0
    num_nodes = 0
    for i in organism.muscles:
        for x in i.nodes:
           x_val += x.xy[0]
           num_nodes += 1
    
    avg_x_val = x_val/num_nodes

    return avg_x_val