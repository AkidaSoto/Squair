# Squair

Sqi[ai]r
A pet square that is self learning but also can be taught.

The square is in a grid. It can see one space in all directions and can move one space in any direction. The idea is for it to only know to navigate the world, assign value to objects and remember the past. 

We will eventually put objects on the map the square can interact with. These will reward or punish the square. It will learn to associate the actions it took that lead to that outcome as well as the environment that lead to that specific outcome. It will remember that information and will try to either increase or decrease the likelihood of the outcome in the future.

This will be done by using SARSA or Reinforcement Learning algorithms. What's cool about these models is that only activated nodes and it's connections are modified so there's no reactive updating of previous or inactive variables (That any basic ML would do). Despite that, the model is still able to learn and adjust behaviors by proactively anticipating actions and rewards.

Sequence of actions:

1. Determine the POLICY (action plan) to do:
  - surrounding tile (implemented): look at the surrounding tiles and their reward history
  
  - to be implemented (beginner):
  - cardinal direction: look at the cartesian plane and their reward history
  - relative face: look at it's relative position and the reward history
  - internal state: some kind of hunger state?

  - to be implemented (advanced):
  - Policy creation/policy fusion: see a.
  - Rumination (action do nothing but applyoff-policy RL): see b.

1. Depending on the POLICY, determine it's current STATE and if it has a history with it. 
  - If not, make a new STATE memory node.
  - If yes, recall that STATE memory node. 

  - to be implemented:
  - If possible to create some kind of state-chunking?: see a.

2. Determine the possible decisions to make in the STATE
  - There are 8 possible directions to go in
     - some policy can have repeition or choices that share reward history 

  - to be implemented:
  - Action chunking, action creation: see c.

  - Use a softmax equations using predicted REWARDS to determine the liklihood to move in any direction. Pick ACTION.

3. Execute decision

4. Assess feedback. 
  - Calculate the OUTCOME
  - Compare OUTCOME to predicted REWARD from chosen ACTION of a STATE given a policy
     - compute prediction error
  - Update REWARD for 
     - POLICY-STATE-ACTION-REWARD pairing memory node

TO DO:

Addition RL functions
Add in an option to “train” the square by external reward/punishment from the user (REWARD override)

A.) Feature Detection:
This papers talks about value transfer when switching between different policy:
https://www.nature.com/articles/s41598-017-17687-2#Fig2
So they talk about policy fusion but they don't talk about policy creation or state chunking. 
It's still a start though.

Spacial state chunking seems like visual chunking but temporal state chunking seems like model-based learning or state-transition memory? 

B.) Rumination:
The idea of not doing anything but thinking and modifiying a plan by projecting hypotheticals is a part of living creatures!
Implementing some kind of history recall system (Long and Short-term memory?) and off-policy RL applications seems like the way to do that.
https://kowshikchilamkurthy.medium.com/off-policy-vs-on-policy-vs-offline-reinforcement-learning-demystified-f7f87e275b48

C.) Habit formation over rides reward contingency changes (Action Chunking for Sequential Learning):
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3325518/ 

Gaming Features:

Reward View: Each tile has the reward value visible for user
Eating should be a seperate action?


FORMULAS

from:  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2895323/
Model-Free learning (for STATE-ACTION-REWARD)
  - δRPE = R - QSARSA(s, a)
  - QSARSA(s, a) = QSARSA(s, a) + αδRPE

State Learning (for STATE-ACTION-STATE)
  - δSPE = 1 − T(s, a, s′)
  - T(s, a, s′) = T(s, a, s′) + ηδSPE
  - QFWD(s,a)=∑s′T(s,a,s′)×(r(s′)+argmaxa′QFWD(s′,a′))
HYBRID Learner
  - wt = l × e−kt
  - QHYB(s, a) = wt × QFWD(s, a) + (1 − wt) × QSARSA(s, a)

SOFTMAX EQUATION for any decision models
  - P(s,a)=exp(τ×Q(s,a))∑nb=1exp(τ×Q(s,b))


Thoughts for myself:
    The softmax equation acts pretty odd when Q values are not 1?
    Relative values if Q were [0,10] could simplify to [0,1]?
    Should R be => R/max(R)?
    This wouldn't translate well when comparing Q's that originally had different Rs? Max(R) implies a unique memory node for REWARDS?

    Is magnitude of prediction error related to alpha learning rate? alpha already modifies prediction error which collectively modifies Q so would it be too recursive for prediction error to also affect alpha?
    Or could we say that positive prediction error reduces connections of inactive Q while negative prediction errors increases connections of inactive Qs? The softmax equation already makes it as a default that decreased Q increases exploration.