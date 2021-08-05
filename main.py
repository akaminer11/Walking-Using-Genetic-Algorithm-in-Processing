import math
from creatureFiles import *
from evolution import *
from recombination import *
from selection import *

'''
R:
Muscles *
Nodes

* = completed

Organism:
    Genes:
    Internal rhythm *
    Muscles: *
        Relaxed Length *
        Contracted Length *
        Rhythm of contraction *
        Connections to nodes *
        Strength *
    Nodes:
        Number of nodes *
        Friction *
    Generator *
    

Physics: *
    Gravity *
    Ground collision *
    Obstacle collision *
    Friction *
    
Gene mixing
Fitness definition (easy):
    How far to the right it makes it
    
Graphical simulation (necessary?)
Choosing the fittest 
Obstacle editor
'''

'''
Nodes: position (xy = [x, y]) and friction (0 to 255) as starting values, vXY for updating position

Muscles: nodes ([node1, node2]) that it anchors to, strength of the muscle (strength = 0 to 255), how long its cycle is in total (probably gonna be frames), and a range ([0 to 1, 0 to 1]) that defines what portion of the cycle the muscle will spend contracted
(muscles have no collision, they might clip through the ground)

Organism: has muscles as an input, doesn't need nodes because nodes are already considered in the muscles. Remember that different muscles can be anchored to the same node
'''

numCreatures = 100
timer = 0
startTimer = 0
organisms = []
ground = []
curScreen = 1 # 0 = title screen, 1 = menu screen, 2 = simulation screen
screenTranslate = [640, 720]
offset = [0, 0]
generations = 0
generationalFitness = []
organismsByGeneration = []
scrollerX = 50
PERCENT_ELITES = 10
TIME = 30
TOTAL_FRAMES = TIME * 60
GEN_SIZE = 10
gravity = 0.2
dt = 1
graphSize = 200

savedInfo = open('savedGenes.txt', 'w')
loadedInfo = open('genesToLoad.txt', 'r')

groundResolution = 20
for i in range(-120*groundResolution, 168*groundResolution+1):
    ground.append([180*i/groundResolution, 350 + .5*(250-500*noise((0.5*i/groundResolution)))])


node1 = Node([200, 200], [0, 0], 100)
node2 = Node([400, 400], [0, 0], 50)
node3 = Node([200, 300], [0, 0], 255)
node4 = Node([500, 250], [0, 0], 200)
muscle1 = Muscle([node1, node2], 200, 400, 5, 240, [0.0, 0.5])
muscle2 = Muscle([node2, node3], 200, 400, 5, 240, [0.5, 1.0])
muscle3 = Muscle([node1, node3], 400, 600, 5, 140, [0.2, 0.8])
muscle4 = Muscle([node1, node4], 400, 600, 5, 140, [0.2, 0.8])
muscle5 = Muscle([node2, node4], 200, 400, 5, 140, [0.2, 0.8])
muscle6 = Muscle([node3, node4], 200, 400, 5, 140, [0.2, 0.8])
organism1 = Organism([muscle1, muscle2, muscle3, muscle4, muscle5, muscle6], 0)

node5 = Node([0, 100], [5, 0], 0)
node6 = Node([100, 100], [5, 0], 0)
muscle7 = Muscle([node5, node6], 100, 100, 0, 100, [0.5, 1.0])

car = Organism([muscle7], 0)

organisms = []

for i in range(numCreatures):
    organisms.append(generateOrganism())     

def gradient(color1, color2, rectangle):
    for i in range(100):
        noStroke()
        fill(color1[0] + 1.0 * i*(color2[0] - color1[0])/100, color1[1] + 1.0 * i/(color2[1] - color1[1]), color1[2] + 1.0 * i/(color2[2] - color1[2]))
        rect(rectangle[0], rectangle[1] + 1.0*i*rectangle[3]/100.0, rectangle[2], 1.0*rectangle[3]/100.0)

def setup():
    size(1280, 720)
    background(255)
    
curScreen = 0
curGen = 0
organismsByGeneration.append(organisms)
fitnesses = []
for i in range(numCreatures):
    fitnesses.append(organisms[i].fitness)
generationalFitness.append(fitnesses)
def draw():
    global timer
    global startTimer
    global organisms
    global ground
    global curScreen
    global screenTranslate
    global generations
    global generationalFitness
    global organismsByGeneration
    global curGen
    global gravity
    global dt
    global graphSize
    if timer % 60 == 0:
        #print('still alive ' + str(timer) + ', we are looking at creature ' + str(organismsByGeneration[curGen][0]))
        pass
    if curScreen == 0:
        background(255)
        textSize(40)
        stroke(0)
        fill(0)
        textAlign(CENTER, CENTER)
        text('Simulation of Evolution of Creatures', width/2, height/2 - 140)
        text('Walking Over an Uneven Surface', width/2, height/2 - 90)
        fill(40, 160, 60)
        strokeWeight(2)
        rect(width/2 - 120, height/2 + 20, 240, 100) # start button
        rect(width/2 - 120, height/2 + 180, 240, 100) # simulate generation
        fill(0)
        text('Start', width/2, height/2 + 63)
        text('Load File', width/2, height/2 + 223)
        if mousePressed and mouseX > width/2 - 120 and mouseX < width/2 + 120 and mouseY > height/2 + 20 and mouseY < height/2 + 120:
            curScreen = 1
        if mousePressed and mouseX > width/2 - 120 and mouseX < width/2 + 120 and mouseY > height/2 + 180 and mouseY < height/2 + 280:
            pass
            '''curScreen = 1
            generations = int(loadedInfo.readLine())
            numGenerations = int(loadedInfo.readLine())
            generationSize = int(loadedInfo.readLine())
            for i in range(numGenerations):
                for j in range(generationSize):
                    orgFitness = double(loadedInfo.readLine())
                    numMuscles = int(loadedInfo.readLine())
                    for k in range(numMuscles):'''
                        
                    
            
    if curScreen == 1:
        background(214)
        scale(0.5)
        screenTranslate = [3850 - organismsByGeneration[curGen][0].avgPos(), 1400]
        simulate(organismsByGeneration[curGen][0], ground, gravity, 1, timer, groundResolution, screenTranslate)
        #simulate(car, ground, gravity, 1, timer, groundResolution, screenTranslate)
        translate(-screenTranslate[0], -screenTranslate[1])
        scale(4.0)
        fill(214)
        noStroke()
        rect(0, 0, width - 575, height)
        rect(0, 496, width, height - 100)
        rect(width - 50, 0, 100, height)
        rect(0, 0, width, 200)
        fill(40, 160, 60)
        strokeWeight(2)
        stroke(0)
        textSize(40)
        textAlign(LEFT)
        rect(width - 575, 30, 525, 65) # simulate generation
        rect(width - 575, 115, 525, 65) # continuous sim
        rect(width - 575, 520, 525, 65) # save results
        rect(width - 575, 605, 525, 65) # view creature
        noFill()
        rect(width - 575, 200, 525, 297) # creature box
        fill(255)
        rect(width - 1225, 520, 525, 65) # graph label
        rect(width - 1225, 200, 525, 295) # graph
        rect(width - 575, 200, 525, 65) # creature box label
        fill(0)
        text("Simulate Generation", width - 500, 75)
        text("Continuous Quick Sim", width - 520, 160)
        text("Best Creature", width - 435, 250)
        text("Save Results", width - 430, 565)
        text("View Creature", width - 445, 650)
        text("Fitness Over Time", width - 1140, 565)
        textSize(70)
        text("Generation " + str(curGen), 50, 100)
        #text("total number of organisms: " + str(len(organismsByGeneration)*len(organismsByGeneration[0])), 50, 600)
        stroke(0)
        strokeWeight(5)
        line(50, 160, 560, 160)
        strokeWeight(5)
        line(width - 1224, 200 + 295/2, width - 1224 + 523.0, 200 + 295/2)
        strokeWeight(3)
        for i in range(1, len(organismsByGeneration)):
            line(width - 1224 + 523.0*(i-1)/(len(organismsByGeneration)-1), 200 + 295/2 - organismsByGeneration[i-1][0].fitness * 100.0/graphSize, width - 1224 + 523.0*i/(len(organismsByGeneration)-1), 200 + 295/2 - organismsByGeneration[i][0].fitness * 100.0/graphSize)
            textAlign(CENTER)
            textSize(15)
            if(i % int(len(organismsByGeneration)/10+1) == 0):
                text(int(organismsByGeneration[i][0].fitness), width - 1224 + 523.0*(i)/(len(organismsByGeneration)-1), 200 + 295/2 - organismsByGeneration[i][0].fitness * 100.0/graphSize)
        fill(100)
        if generations == 0:
            rect(50, 140, 20, 40)
        else:
            for i in range(generations+1):
                if scrollerX <= 50 + 490.0 * (2.0*i + 1)/(2*generations):
                    rect(50 + 490.0 * i/(generations), 140, 20, 40)
                    if i != curGen:
                        organismsByGeneration[curGen][0].resetNodes()
                        timer = 0
                    curGen = i
                    break
        #print(generationalFitness)
        #print(curGen)
    if curScreen == 2:
        scale(1)
        simulate(organismsByGeneration[curGen][0], ground, gravity, 1, timer, groundResolution, screenTranslate)
        #simulate(car, ground, gravity, 1, timer, groundResolution, screenTranslate)
        fill(40, 160, 60)
        strokeWeight(4)
        stroke(0)
        rect(width - screenTranslate[0] + 650, 100 - screenTranslate[1], 525, 130)
        fill(0)
        textSize(80)
        text("Return", width - screenTranslate[0] + 910, 150 - screenTranslate[1])
    
    if curScreen == 4:
        genFitness = []
        genOrganisms = []
        for i in range(600):
            print(i)
            for j in organisms:
                j.updateNoDraw(dt, i, gravity, ground, groundResolution)
        for i in organisms:
            x_val = 0.0
            num_nodes = 0
            for j in i.muscles:
                for x in j.nodes:
                    x_val += x.xy[0]
                    num_nodes += 1
            avg_x_val = x_val/num_nodes
        
            # updates the individual's fitness
            i.fitness = avg_x_val - 500
            i.resetNodes()
            genFitness.append(i.fitness)
            genOrganisms.append(i)
        genOrganisms = sort_by_fitness(organisms)
        genFitness.sort()
        genFitness.reverse()
        generationalFitness.append([genFitness[0]])
        organismsByGeneration.append([genOrganisms[0]])
        if abs(organisms[0].fitness) > graphSize:
            graphSize = abs(int(organisms[0].fitness/100)*100) + 100
        organisms = run_generation(organisms)
        curScreen = 1
        generations += 1
        for i in organismsByGeneration:
            for j in i:
                for k in j.muscles:
                    for l in k.nodes:
                        l.xy[0] = l.originalXY[0]
                        l.xy[1] = l.originalXY[1]
        for i in range(len(generationalFitness)):
            print('gen ' + str(i) + ': ' + str(generationalFitness[i]))
        timer = 0
        
    timer += 1
    textSize(50)
    
def mouseReleased():
    global curGen
    global curScreen
    global scrollerX
    
    if curScreen == 1:
        if generations == 0:
            divisor = 1
        else:
            divisor = generations
        scrollerX = 1.0 * curGen/divisor * 490.0 + 50.0

def mousePressed():
    global offset
    global scrollerX
    global curScreen
    global dt
    global gravity
    global ground
    global groundResolution
    global screenTranslate
    if curScreen == 1:
        offset = [mouseX - scrollerX, 0]
        if mouseX >= scrollerX and mouseX <= scrollerX + 20 and mouseY >= 140 and mouseY <= 180:
            offset[1] = 1
        else:
            offset[1] = 0
        if mouseX >= width - 575 and mouseX <= width - 50 and mouseY >= 605 and mouseY <= 670:
            curScreen = 2
            screenTranslate = [720, 720]
        if mouseX >= width - 575 and mouseX <= width - 50 and mouseY >= 30 and mouseY <= 95:
            curScreen = 4
        if mouseX >= width - 575 and mouseX <= width - 50 and mouseY >= 520 and mouseY <= 585:
            savedInfo.write(str(generations) + '\n')
            savedInfo.write(str(len(organismsByGeneration)) + '\n')
            savedInfo.write(str(len(organismsByGeneration[0])) + '\n')
            for j in range(len(organismsByGeneration[0])):
                savedInfo.write(str(organismsByGeneration[-1][j].fitness) + '\n')
                savedInfo.write(str(len(organismsByGeneration[-1][j].muscles))+ '\n')
                for k in range(len(organismsByGeneration[-1][j].muscles)):
                    savedInfo.write(str(organismsByGeneration[-1][j].muscles[k].contractLength) + '\n')
                    savedInfo.write(str(organismsByGeneration[-1][j].muscles[k].relaxLength) + '\n')
                    savedInfo.write(str(organismsByGeneration[-1][j].muscles[k].strength) + '\n')
                    savedInfo.write(str(organismsByGeneration[-1][j].muscles[k].timerLength) + '\n')
                    savedInfo.write(str(organismsByGeneration[-1][j].muscles[k].cycle[0]) + '\n')
                    savedInfo.write(str(organismsByGeneration[-1][j].muscles[k].cycle[1]) + '\n')
                    
                    for l in range(2):
                        savedInfo.write(str(organismsByGeneration[-1][j].muscles[k].nodes[l].xy[0]) + '\n')
                        savedInfo.write(str(organismsByGeneration[-1][j].muscles[k].nodes[l].xy[1]) + '\n')
                        savedInfo.write(str(organismsByGeneration[-1][j].muscles[k].nodes[l].vXY[0]) + '\n')
                        savedInfo.write(str(organismsByGeneration[-1][j].muscles[k].nodes[l].vXY[1]) + '\n')
                        savedInfo.write(str(organismsByGeneration[-1][j].muscles[k].nodes[l].friction) + '\n')
                savedInfo.write('\n')
    if curScreen == 2:
        offset = [2*mouseX - screenTranslate[0], 2*mouseY - screenTranslate[1]]
        if mouseX >= 965 and mouseX <= 1225 and mouseY > 40 and mouseY < 105:
            organismsByGeneration[curGen][0].resetNodes()
            curScreen = 1

def mouseDragged():
    global curScreen
    global screenTranslate
    global offset
    global scrollerX
    if curScreen == 1:
        if offset[1] == 1:
            scrollerX = mouseX - offset[0]
        if scrollerX < 50:
            scrollerX = 50
        if scrollerX > 540:
            scrollerX = 540
    if curScreen == 2:
        screenTranslate[0] = 2*mouseX - offset[0]
        screenTranslate[1] = 2*mouseY - offset[1]
    


'''
Day 1: 6/29/21

Richard:
    Made the classes for nodes, muscles, organisms, still need work on them
    Defined the way they interact, set up for later muscle contraction, etc
    Started work on physical interaction (gravity)

Andrew:
    Made the select_fittest module. It has a bunch of functions, but the main function is select_fittest(). It takes a list of individuals after a generation has been run. It returns a new list of individuals selected to reproduce. Also started work on the generate_new_individuals module


Day 2: 6/30/21

Richard:
    Finished the muscle contractions and fixed gravity
    Patched a bug where once nodes hit the ground, they're stuck
    Added in air friction and ground friction
    Started up the physics module for the nodes
    Created a creature generator (needs work)

Andrew: Started work on the generation module to generate new organisms to replace those culled by the selection module.


Day 3: 7/1/21

Richard:
    Started working on a rough ground and collision

Andrew:
    Finished generation module and did some review of both the generation and selection modules.
    

Day 4: 7/2/21

Richard:
    Finished ground collisions
    

Day 5: 7/5/21

Richard:
    Made the main menu screen, working on the regular menu screen


Day 6: 7/6/21

Richard:
    Mostly finished the menu screen, started putting together the different parts of the program
'''