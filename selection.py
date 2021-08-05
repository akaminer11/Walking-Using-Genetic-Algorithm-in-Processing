"""
\nEffectively responsible for culling the generation, based on fitness. The main function of this module is select_fittest(). It takes a list of individuals after a generation has been run. It returns a new list of
individuals selected to reproduce. 
\nList of functions: select_fittest(list, p); sort_by_fitness(list); ret_percent_of_max_fitness(max, individual); quick_sort(list, low, high);
partition(list, low, high); swap(list, a, b)
"""
from random import randint
WEIGHT = 2 # The number that determines how hard it is for non-elites to survive to the next gen. Higher makes it harder for non-elites.

def random(num): # DONE
    """
    Returns a random int from 0 to the entered num (inclusive)
    """
    return randint(0,num)


def select_fittest(l, p): # DONE 
    '''
    Takes a SORTED list of individuals (by fitness), and selects the top p percent as elites, which have a double chance of mating.
    Returns a list of the selected individuals. Mating/generation of new ones should be done seperately.
    '''
    global WEIGHT
    num_individuals = len(l)
    num_to_be_autoselected = int(num_individuals * p / 100)
    new_list_of_individuals = []

    new_list_of_individuals = l[:num_to_be_autoselected]

    # iterates through the non-elites. For each individual, it generates a random percent of 100. If the percent of random fitness, divided by 
    # weight, is larger than the random number, then the individual is appended to the new list.
    for i in l[num_to_be_autoselected:]:
        percent = ret_percent_of_max_fitness(l[0].fitness, i)
        r = random(100)/100.0
        if percent / WEIGHT > r:
            new_list_of_individuals.append(i)

    return new_list_of_individuals


def sort_by_fitness(l): # DONE
    """
    Takes list of individuals after a test. Goes through the list and sorts them by fitness. Uses quicksort.
    Returns sorted list.
    """
    l.sort(key=lambda x: x.fitness, reverse=True)
    return l


def ret_percent_of_max_fitness(max, individual): # DONE
    """
    Takes the maximum fitness of an individual in the generation and a specific individual. 
    Returns the percentage of the max fitness.
    """
    return 1.0 * individual.fitness / max