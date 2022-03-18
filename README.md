# Squair

A pet square that is self learning but also can be taught.

The square is in a grid. It can see one space in all directions and can move one space in any direction.  

The idea is for it to only know to navigate the world, assign value to objects and remember the past. 

We will eventually put objects on the map the square can interact with. These will reward or punish the square. It will learn to associate the actions it took that lead to that outcome as well as the environment that lead to that specific outcome. It will remember that information and will try to either increase or decrease the liklihood of the outcome in the future.

Sequence of actions:

1. Assess the surroundings. The square looks around and see if the pattern of objects (the CONTEXT) around it is familiar. 
  - If not, make a new CONTEXT memory node.
  - If yes, remember that CONTEXT memory node. 

2. Determine the possible decisions to make in this CONTEXT
  - There is 9 possible directions to go in
     - each direction is a STATE memory node
    
  - If old CONTEXT recall the REWARD for each STATE memory node⋅⋅
  - If old CONTEXT recall the STATE transition for each STATE memory node.

  - Use a softmax equations using REWARDS to determine the liklihood to move in any direction. Pick ACTION.

3. Execute decision

4. Assess feedback. 
  - Calculate the OUTCOME
  - Compare OUTCOME to REWARD from chosen ACTION of a STATE   
     - compute prediction error
  - Update REWARD for 
     - CONTEXT-STATE-ACTION-REWARD pairing memory node
     - ⋅STATE-ACTION-REWARD pairing memory node
     - STATE-REWARD pairing memory node
     - STATE-ACTION-STATE transition pairing memory node


Addition functions

Memory nodes for individual spaces it can move on. 

CONTEXT memory loads are efficient by reorienting the space from the direction the square moved in. 

Add in an option to “train” the square by external reward/punishment from the user (REWARD override)


FORMULAS

from:  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2895323/

Model-Free learning (for STATE-ACTION-REWARD)
δRPE = R - QSARSA(s, a)
QSARSA(s, a) = QSARSA(s, a) + αδRPE

State Learning (for STATE-ACTION-STATE)
δSPE = 1 − T(s, a, s′)
T(s, a, s′) = T(s, a, s′) + ηδSPE

QFWD(s,a)=∑s′T(s,a,s′)×(r(s′)+argmaxa′QFWD(s′,a′))

HYBRID Learner
wt = l × e−kt
QHYB(s, a) = wt × QFWD(s, a) + (1 − wt) × QSARSA(s, a)

SOFTMAX EQUATION for any decision models
P(s,a)=exp(τ×Q(s,a))∑nb=1exp(τ×Q(s,b))