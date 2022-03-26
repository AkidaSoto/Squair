import math
import numpy as np
import random

class TraditionalRL():

    def _init_(self):
        super(TraditionalRL, self).__init__()
        
        # This is the square it is on
        self.Ss = [] 
        
         # This is the Policy that the square will enact (which features)
        self.Ps = ['type' 'direction' 'facing']
        
        self.defaultP = 0
        
        # This is the type of action it has learned/seen from the Policy outcome
        self.As = []
        
        # This is the outcome learned/seen 
        self.Qs = []

        self.alpha = .5
        self.beta = 30

    def CheckState(self,player):

        if player.Center.type not in self.Ss:
            newStateidx = len(self.Ss)
            
            self.Ss.append(player.Center.type)
            self.As.append([[],[],[]])
            self.Qs.append([[],[],[]])
            
            # Insert Cardinal Directions
            
            for direction in range(0,8):
                action = {'x':0,'y':0}
                action['x'] = round(math.sin(math.radians(direction*45)))
                action['y'] = round(math.cos(math.radians(direction*45)))
                self.As[newStateidx][1].append(action)
                self.Qs[newStateidx][1].append(0)
        
        for idx in range(len(self.Ss)):
            if player.Center.type == self.Ss[idx]:
                
                 #check Type
                for surround in player.Surround:
                    if surround.type not in self.As[idx][0]:
                        self.As[idx][0].append(surround.type)
                        self.Qs[idx][0].append(0)
                        
                return idx

    def makeAction(self,player):

        idx = self.CheckState(player)
        
        #collect the choice Qs
        
        QArray = []
        AArray = []
        for surround in player.Surround:
            for Qidx in range(len(self.As[idx][self.defaultP])):
                if surround.type == self.As[idx][self.defaultP][Qidx]:
                    QArray.append(self.Qs[idx][self.defaultP][Qidx])
                    AArray.append(self.As[idx][self.defaultP][Qidx])

        
        start = 0
        Parray = []
        for Pa in range(len(QArray)):
            num = math.exp(self.beta*QArray[Pa])
            dem = np.sum(np.exp(self.beta*np.array(QArray)))
            P = num/dem
            Parray.append(start+(P))
            start += P
        
        prob = random.random()
        actionidx = np.argmax(prob < np.array(Parray))
        action = self.As[idx][1][actionidx]
        actiontype = AArray[actionidx]
        
        return idx, actiontype, action

    def updateExpectation(self,Stateidx,actiontype, Outcome):
        
        for action in range(len(self.As[Stateidx][self.defaultP])):
            if self.As[Stateidx][self.defaultP][action] == actiontype:
                actionidx = action
        
        predictionerror = Outcome -  self.Qs[Stateidx][self.defaultP][actionidx]
        self.Qs[Stateidx][self.defaultP][actionidx] += self.alpha*predictionerror

