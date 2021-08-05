"""
Module for taking a list that has been culled by the select_fittest() function and generating new individuals. Most important function is mate_list(). It takes a culled list and returns one filled in with new organisms.
\nList of functions: random(), how_many_to_add(), mate_list, mate(), mate_muscle(), mutate(), mutate_length(), gen_new_node(), handle_node_generation().
"""

from random import randint, uniform
from creatureFiles import Organism, Muscle, Node# I'm going to assume that the class for organisms will be importable

MUTATION_CHANCE = 10
NEW_NODE_CHANCE = 2
minMutate = 80.0
maxMutate = 45.0

def mutate_everything(l):
    for i in range(len(l)):
        for m in range(i % 4):
            l[i] = gen_new_node(l[i], NEW_NODE_CHANCE)
            l[i] = remove_node(l[i], NEW_NODE_CHANCE)
            for j in l[i].muscles:
                for k in j.nodes:
                    k.friction += (random(40)) - 20
                    k.friction *= (minMutate + random(maxMutate))/100
                    if k.friction > 255:
                        k.friction = 255
                    if k.friction < 0:
                        k.friction = 0
                j.contractLength += random(100) - 50
                j.contractLength *= (minMutate + random(maxMutate))/100
                j.relaxLength += random(100) - 50
                j.relaxLength *= (minMutate + random(maxMutate))/100
                j.strength += random(100) - 50
                j.strength *= (minMutate + random(maxMutate))/100
                j.timerLength += random(40) - 20
                j.timerLength *= (minMutate + random(maxMutate))/100
                
                if j.contractLength < 100:
                    j.contractLength = 100
                if j.contractLength > 600:
                    j.contractLength = 600
                    
                if j.relaxLength < 100:
                    j.relaxLength = 100
                if j.relaxLength > 600:
                    j.relaxLength = 600
                    
                if j.strength > 1000:
                    j.strength = 1000
                if j.strength < 0:
                    j.strength = 0
                
                if j.timerLength > 300:
                    j.timerLength = 300
                if j.timerLength < 30:
                    j.timerLength = 30
                
                j.cycle[0] += 1.0*random(20)/100.0 - 0.1
                j.cycle[0] *= (minMutate + random(maxMutate))/100
                j.cycle[1] += 1.0*random(20)/100.0 - 0.1
                j.cycle[1] *= (minMutate + random(maxMutate))/100
                if j.cycle[0] > 1:
                    j.cycle[0] = 1
                if j.cycle[1] > 1:
                    j.cycle[1] = 1
                if j.cycle[0] < 0.2:
                    j.cycle[0] = 0.2
                if j.cycle[1] < 0.2:
                    j.cycle[1] = 0.2
                
                a = max(j.cycle[0], j.cycle[1])
                b = min(j.cycle[0], j.cycle[1])
                j.cycle[0] = b
                j.cycle[1] = a
    return l
            

def random(num): # DONE
    """
    Returns a random int from 0 to the entered num (inclusive)
    """
    return randint(0,num)


def how_many_to_add(l, original_number): # DONE
    """
    Utility function to return how many new individuals need to be generated.
    """
    return original_number - len(list)


def mate_list(culled_list, num_elites, num_to_be_added): # DONE. Check for logic errors.
    """
    Takes a list has been culled by the selection module, the number of elites, and the number to be added. Fills the list with the offspring of
    randomly selected individuals, with elites weighed better. Assumes that the list is still sorted by fitness.
    """

    new_list_length = len(culled_list) + num_to_be_added

    new_list = culled_list

    # Ok this part is kind of a mess.
    # For every organism that needs to be added to the list, it selects a random number, the size of the culled list + the number of elites.
    # If the number is > the length of the culled list, it subtracts that length. This way, the elites get double the chance of mating. The selected
    # organism is the one with the index in the culled list of the random number. It does this a second time to select the partner.
    for i in range(num_to_be_added):
        orgA_index = random(len(culled_list) + num_elites - 1) % len(culled_list)
        orgA = culled_list[orgA_index]

        orgB_index = random(len(culled_list) + num_elites - 1) % len(culled_list)
        orgB = culled_list[orgB_index]
        

        # Generates a new organism and adds it to the new list.
        new_list.append(mate(orgA, orgB))

    return new_list
        

def mate(orgA, orgB): # DONE, probably. Check for logical problems.
    """
    Takes two organisms and randomly choose traits from both of them to pass on to the next generation
    """
    # randomly chooses one of the parents to base the new organism off of. Fitness to start is None. It should be calculated after every round,
    # so this should work.
    if 50 > random(100): 
        orgC = orgA
    else:
        orgC = orgB
    '''newMuscles = []
    for j in orgC.muscles:
        newNodes = []
        for k in j.nodes:
            newNodes.append(k)
        newMuscles.append(Muscle(newNodes, j.contractLength, j.relaxLength, j.strength, j.timerLength, j.cycle))
    orgC = Organism(newMuscles, None)'''
    

    # loop through each of the muscles and randomly exchange genes
    if len(orgA.muscles) <= len(orgB.muscles):
        m = len(orgA.muscles)
    else:
        m = len(orgB.muscles)
    for muscle_index in range(m):
        muscleA = orgA.muscles[muscle_index]
        muscleB = orgB.muscles[muscle_index]
        
        orgC.muscles[muscle_index] = mate_muscle(muscleA, muscleB)
    
    # determine if a new node is to be generated, and generate it and the accompanying muscle
    #orgC = gen_new_node(orgC, NEW_NODE_CHANCE)

    return orgC


def mate_muscle(muscleA, muscleB): # DONE, I think
    """
    Takes two muscles. Returns a new muscle. Combines traits from two different muscles.\n
    Goes through each of the attributes that a muscle has, excluding nodes, which will be handled seperately and randomly chooses one from the two
    muscles. 
    """
    # selects contracted length
    r = random(1)
    if r == 1:
        contract_length = muscleA.contractLength
    elif r == 0:
        contract_length = muscleB.contractLength
    else:
        print("ERROR: mate_muscle() {r} con")

    # selects relaxed length
    r = random(1)
    if r == 1 or (muscleA.relaxLength >= contract_length and muscleB.relaxLength < contract_length):
        relaxed_length = muscleA.relaxLength
    elif r == 0 or (muscleB.relaxLength >= contract_length and muscleA.relaxLength < contract_length):
        relaxed_length = muscleB.relaxLength
    else:
        print("ERROR: mate_muscle() {r} rel")

    # selects strength
    r = random(1)
    if r == 1:
        strength = muscleA.strength
    elif r == 0:
        strength = muscleB.strength
    else:
        print("ERROR: mate_muscle() {r} str")
    
    # selects timer length
    r = random(1)
    if r == 1:
        timer_length = muscleA.timerLength
    elif r == 0:
        timer_length = muscleB.timerLength
    else:
        print("ERROR: mate_muscle() {r} tim")

    # selects cycle
    r = random(1)
    if r == 1:
        cycle = muscleA.cycle
    elif r == 0:
        cycle = muscleB.cycle
    else:
        print("ERROR: mate_muscle() {r} cyc")

    nodes = muscleA.nodes
    
    r = random(1)
    if r == 1:
        nodes[0].xy = muscleA.nodes[0].xy
        nodes[1].xy = muscleA.nodes[1].xy
        nodes[0].originalXY = muscleA.nodes[0].originalXY
        nodes[1].originalXY = muscleA.nodes[1].originalXY
        nodes[0].friction = muscleA.nodes[0].friction
        nodes[1].friction = muscleA.nodes[1].friction
    else:
        nodes[0].xy = muscleB.nodes[0].xy
        nodes[1].xy = muscleB.nodes[1].xy
        nodes[0].originalXY = muscleB.nodes[0].originalXY
        nodes[1].originalXY = muscleB.nodes[1].originalXY
        nodes[0].friction = muscleB.nodes[0].friction
        nodes[1].friction = muscleB.nodes[1].friction

    # mutate the contracted and relaxed lengths of the muscle
    contract_length, relaxed_length = mutate_length(contract_length, relaxed_length, MUTATION_CHANCE)

    # return the muscle with the mutated values and possibly a new node
    return Muscle(nodes, contract_length, relaxed_length, mutate(strength, 0, 255, MUTATION_CHANCE), timer_length, mutate(cycle, .1, .6, MUTATION_CHANCE))


def mutate(gene, min, max, mutation_chance): # DONE
    """
    Takes a gene, the minimum and maximum values of the gene, and the mutation chance. If the random check passes, it returns a random value 
    between the two values. 
    """

    if isinstance(gene, list):
        new_gene = []
        for i in gene:
            new_gene.append(mutate(i, min, max, mutation_chance))
        return new_gene

    if isinstance(min, float):
        return uniform(min, max)

    if mutation_chance > random(100):
        return randint(min, max)
    return gene


def mutate_length(contract_length, relaxed_length, mutation_chance): # DONE
    """
    Takes the contracted length, the relaxed length, and the mutation chance.
    \nIf the random check, weighted by the mutation chance, passes, returns new values of contracted length and relaxed length.
    """
    if random(100) <= mutation_chance:
        contract_length *= (80.0 + random(50))/100
        relaxed_length *= (80.0 + random(50))/100
    if contract_length < 100:
        contract_length = 100
    if contract_length > 800:
        contract_length = 800
    if relaxed_length < 100:
        relaxed_length = 100
    if relaxed_length > 800:
        relaxed_length = 800
    return contract_length, relaxed_length

def remove_node(orgC, new_node_chance):
    r = random(100)
    if new_node_chance > r and len(orgC.muscles) > 5:
        print(len(orgC.muscles))
        del(orgC.muscles[int(random(len(orgC.muscles)-1))])
    return orgC

def gen_new_node(orgC, new_node_chance): # DONE
    """
    Takes an organism and the percent chance for a new node. Determines whether or not a new node will be generated and generates it. Returns the
    new version of the organism.
    """
    r = random(100)
    if new_node_chance > r and len(orgC.muscles) < 25:
        orgC.muscles.append(handle_node_generation(orgC))
    return orgC
    

def handle_node_generation(orgC): # DONE
    """
    Generates a new, completely random muscle, connected to a the new organism by one node and with one completely random node. 
    Takes the new organism and returns the new organism with a new node + muscle.
    """
    nodes = []

    # Adds all of the nodes to the list of the organism's total nodes.
    for i in orgC.muscles:
        for j in i.nodes:
            nodes.append(j)
    
    start_node = nodes[random(len(nodes) - 1)]

    # generates a new node
    friction = random(255)
    xy = [random(800) + 50, random(400) - 50]
    v_xy = [0,0]

    new_node = Node(xy, v_xy, friction)
    nodes = [start_node, new_node]

    # generates a new muscle in between the two nodes
    c_length = random(400)
    r_length = random(400)

    a = random(10) / 10.0
    b = random(10) / 10.0

    min_cycle = min(a,b)
    max_cycle = max(a,b)

    cycle = [min_cycle, max_cycle]
    return Muscle(nodes, c_length, r_length, random(1000), random(300), cycle)