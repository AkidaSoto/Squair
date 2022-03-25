import math
import numpy as np
import random

class TraditionalRL():

    def _init_(self):
        super(TraditionalRL, self).__init__()
        self.possibleS = []
        self.possibleA = []

        self.Ss = []
        self.As = []
        self.Qs = []

        self.alpha = 1
        self.beta = 1

        for direction in range(0,7):

            action = self.createAction()
            action['x'] = round(math.sin(math.radians(direction*45)))
            action['y'] = round(math.cos(math.radians(direction*45)))

            self.possibleA.append(action)

        action = self.createAction()
        self.possibleA.append(action)

    def createAction(self):

        move = {'x':0,'y':0}
        return move


    def createState(self,type):
        
        newStateidx = len(self.Ss)
        self.As.append([])
        for As in range(len(self.possibleA)):
            self.As[newStateidx].append(self.possibleA[As])

        self.Qs.append([])
        for Qs in range(len(self.possibleA)):
            self.Qs[newStateidx].append(0)

        self.Ss.append(type)
        self.possibleS.append(type)
        return newStateidx

    def CheckState(self,type):

        if type not in self.possibleS:
            self.createState(type)
        
        for idx in range(len(self.possibleS)):
            if type == self.possibleS[idx]:
                return idx

    def makeAction(self,player):

        idx = self.CheckState(player.Center)
        start = 0
        Parray = []
        for Pa in range(len(self.Qs[idx])):
            num = math.exp(self.beta*self.Qs[idx][Pa])
            dem = np.sum(np.exp(self.beta*np.array(self.Qs[idx])))
            P = num/dem
            Parray.append(start+(P))
            start += P
        
        prob = random.random()
        actionidx = np.argmax(prob < np.array(Parray))
        action = self.As[idx][actionidx]
        return idx, actionidx, action

    def updateExpectation(self,Stateidx,actionidx, Outcome):
        predictionerror = Outcome -  self.Qs[Stateidx][actionidx]
        self.Qs[Stateidx][actionidx] += self.alpha*predictionerror

