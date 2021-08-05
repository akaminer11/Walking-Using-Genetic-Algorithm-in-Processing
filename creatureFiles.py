import math

def printFitness(l):
    total = []
    for i in l:
        total.append(l.fitness)
    total.sort()
    total.reverse()
    print(total)

class Organism:
    def __init__(self, muscles, fitness):
        self.muscles = muscles
        self.fitness = fitness
        self.id = id
    
    def update(self, dt, timer, gravity, ground, groundResolution):
        for i in self.muscles:
            i.update(dt, timer, gravity, ground, groundResolution)
            i.drawSelf()
            i.nodes[0].drawSelf()
            i.nodes[1].drawSelf()
    
    def updateNoDraw(self, dt, timer, gravity, ground, groundResolution):
        for i in self.muscles:
            i.update(dt, timer, gravity, ground, groundResolution)
    
    def resetNodes(self):
        for i in self.muscles:
            for j in i.nodes:
                j.xy[0] = j.originalXY[0]
                j.xy[1] = j.originalXY[1]
    
    def avgPos(self):
        numNodes = 0
        totalval = 0.0
        for i in self.muscles:
            for j in i.nodes:
                numNodes += 1
                totalval += j.xy[0]
        return totalval/numNodes
    
    def returnCopy(self):
        newNodes = []
        newMuscles = []
        for i in range(len(self.muscles)):
            for j in range(len(self.muscles[i].nodes)):
                isNew = True
                nodePos = 0
                for k in range(len(newNodes)):
                    if newNodes[k][0] is self.muscles[i].nodes[j]:
                        isNew = False
                        nodePos = k
                        break
                if isNew:
                    newNodes.append([self.muscles[i].nodes[j], i])
                else:
                    newNodes[nodePos].append(i)
        for i in range(len(self.muscles)):
            newMuscles.append(Muscle([], self.muscles[i].contractLength, self.muscles[i].relaxLength, self.muscles[i].strength, self.muscles[i].timerLength, [self.muscles[i].cycle[0], self.muscles[i].cycle[1]]))
        for i in newNodes:
            i[0] = Node([i[0].xy[0], i[0].xy[1]], [0, 0], i[0].friction)
            for j in range(1, len(i)):
                newMuscles[i[j]].nodes.append(i[0])
        return Organism(newMuscles, self.fitness)

class Muscle:
    #strength between 0 and 1000
    #cycle takes a range ([0.1, 0.6]), which determines which portion of its cycle is contracted
    #if it's within the range, it's contracted
    def __init__(self, nodes, contractLength, relaxLength, strength, timerLength, cycle):
        self.nodes = nodes
        self.contractLength = contractLength
        self.relaxLength = relaxLength
        self.strength = strength
        self.timerLength = timerLength
        self.cycle = cycle
        if cycle[1] < cycle[0]:
            a = cycle[1]
            cycle[1] = cycle[0]
            cycle[0] = a
    
    def midpoint(self, nodes):
        return [(nodes[0].xy[0] + nodes[1].xy[0])/2, (nodes[0].xy[1] + nodes[1].xy[1])/2]
    
    def drawSelf(self):
        stroke(255.0/1000*self.strength, 255.0/1000*self.strength, 0)
        line(self.nodes[0].xy[0], self.nodes[0].xy[1], self.nodes[1].xy[0], self.nodes[1].xy[1])
    
    def contractMuscles(self, dt, timer):
        if ((1.0*timer % self.timerLength)/self.timerLength > self.cycle[0]):
            muscleLength = self.contractLength 
        else:
            muscleLength = self.relaxLength
                
        mid = self.midpoint(self.nodes)
        distancesNode0 = [mid[0] - self.nodes[0].xy[0], mid[1] - self.nodes[0].xy[1]]
        distancesNode1 = [mid[0] - self.nodes[1].xy[0], mid[1] - self.nodes[1].xy[1]]
        
        hypotenuse = math.hypot(2*distancesNode0[0], 2*distancesNode0[1])
        
        if(hypotenuse == 0.0):
            hypotenuse = 0.0001
        multi = (hypotenuse - muscleLength)/(10*hypotenuse)
        distancesNode0[0] *= multi
        distancesNode0[1] *= multi
        distancesNode1[0] *= multi
        distancesNode1[1] *= multi
        
        self.nodes[0].vXY[0] += distancesNode0[0]*self.strength/1000
        self.nodes[0].vXY[1] += distancesNode0[1]*self.strength/1000
        self.nodes[1].vXY[0] += distancesNode1[0]*self.strength/1000
        self.nodes[1].vXY[1] += distancesNode1[1]*self.strength/1000
    
    def update(self, dt, timer, gravity, ground, groundResolution):
        self.contractMuscles(dt, timer)
        self.nodes[0].update(dt, gravity, ground, groundResolution)
        self.nodes[1].update(dt, gravity, ground, groundResolution)

class Node:
    #friction goes 0 to 255
    def __init__(self, xy, vXY, friction):
        self.xy = xy
        self.originalXY = [0, 0]
        self.originalXY[0] = self.xy[0]
        self.originalXY[1] = self.xy[1]
        self.vXY = vXY
        self.friction = friction
    
    def drawSelf(self):
        noStroke()
        fill(0, 255-self.friction, 255-self.friction)
        circle(self.xy[0], self.xy[1], 50)
        #highest friction is black
        
    def physics(self, gravity, ground, groundResolution):
        '''
        -480, -474
        '''
        pos = int(self.xy[0]/(180.0/groundResolution))-168*groundResolution
        
        aboveGround = True
        belowPoint = 0
        for i in range(pos-3, pos+3):
            if math.hypot(self.xy[0] - ground[i][0], self.xy[1] - ground[i][1]) < 25 or self.xy[1] + 25 > ground[i][1]:
                aboveGround = False
                belowPoint = i
                break
        if aboveGround:
            self.vXY[1] += gravity
        else:
            self.xy[1] = ground[belowPoint][1] - 26
            #if self.vXY[1] > 0:
            #    self.vXY[1] *= -1
            self.vXY[0] *= (255.0-self.friction)/(255)
    
    def update(self, dt, gravity, ground, groundResolution):
        self.physics(gravity, ground, groundResolution)
        self.vXY[0] *= 0.95
        self.vXY[1] *= 0.95
        self.xy[0] += self.vXY[0]*dt
        self.xy[1] += self.vXY[1]*dt
        

def generateOrganism():
    muscles = []
    nodes = []
    numNodes = int(random(5)) + 5
    numMuscles = int(random(numNodes * (numNodes-3)/2)) + 1 + numNodes
    possibleConnections = []
    for i in range(numNodes):
        for j in range(i+1, numNodes):
            possibleConnections.append([i, j])
    for i in range(numNodes):
        nodes.append(Node([random(800) + 50, random(400) - 100], [0, 0], random(255)))
    for i in range(numMuscles):
        nodesChosen = int(random(len(possibleConnections)))
        cycle1 = random(1)
        cycle2 = random(1)
        minCycle = min(cycle1, cycle2)
        maxCycle = max(cycle1, cycle2)
        muscle1 = random(400)
        muscle2 = random(400)
        minMuscle = min(muscle1, muscle2)
        maxMuscle = max(muscle1, muscle2)
        muscles.append(Muscle([nodes[possibleConnections[nodesChosen][0]], nodes[possibleConnections[nodesChosen][1]]], minMuscle, maxMuscle, random(1000), random(600)+60, [minCycle, maxCycle]))
        del possibleConnections[nodesChosen]
    return Organism(muscles, 0)

def simulate(organism, ground, gravity, dt, timer, groundResolution, screenTranslate):
    scale(0.5)
    translate(screenTranslate[0], screenTranslate[1])
    background(200)
    fill(255, 0, 0)
    strokeWeight(10)
    stroke(0)
    noStroke()
    for i in range(-50, 50):
        fill(255)
        rect(500+2000 * i - 20, -200, 40, 800)
        rect(500+2000 * i - 280, -200, 560, 200)
        fill(0)
        textAlign(CENTER, CENTER)
        textSize(100)
        text(str(10*i) + " M", 500 + 2000*i, -120)
    organism.update(dt, timer, gravity, ground, groundResolution)
    '''car.update(1, timer, gravity, ground)
    car.muscles[0].nodes[0].vXY[0] = 1
    car.muscles[0].nodes[1].vXY[0] = 1'''
    timer += dt
    for i in range(len(ground)-1):
        strokeWeight(15)
        stroke(40, 160, 60)
        x = organism.avgPos() - ground[i][0]
        if x < 4000 and x > -4000:
            line(ground[i][0], ground[i][1], ground[i+1][0], ground[i+1][1])
            line(ground[i][0], ground[i][1], ground[i][0], height+500)