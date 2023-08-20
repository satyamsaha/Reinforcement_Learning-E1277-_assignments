
import numpy as np
import math

class Maze:
    def __init__(self, gridHeight=6, gridWidth=6, terminalReward=10, lockPickProb=0.5):
        self.rewardsLeft = np.array([[-1, 0, 0, 0, 0, 0], 
                                    [-1, -1, 0, 0, 0,-10], 
                                    [-1, 0, 0, -1, -1, -1], 
                                    [0, 0, 0, -10, -1, -1],
                                    [-1, -1, 0, 0, -1, 0],
                                    [-1, 0, -1, 0, 0 ,-1]])

        self.rewardsRight =  np.array([[ 0, 0, 0, 0, 0, -1], 
                            [ -1, 0, 0 , 0, -10, -1],
                            [ 0, 0, -1, -1, -1, -1],
                            [ 0, 0, -10, -1, -1 ,-1],
                            [ -1, 0, 0, -1, 0, -1],
                            [ 0, -1, 0, 0, -1, -1]])

        self.rewardsUp  =  np.array([[ -1, -1, -1, -1, -1, -1], 
                            [ 0, -1, -1, -1, -1, 0],
                            [ 0, 0, -1, 0, 0, 0],
                            [ -1, 0,0, 0,0, 0],
                            [ 0, -10, -1, -1, -1, 0],
                            [ 0,  0, -1, -10, 0, 0]])


        self.rewardsDown =  np.array([[ 0, -1, -1, -1, -1, 0], 
                            [ 0, 0, -1, 0, 0, 0],
                            [ -1, 0, 0, 0, 0, 0],
                            [ 0, -10,-1,-1,-1, 0],
                            [  0,0,-1,-10,0, 0],
                            [ -1, -1, -1, 0, -1, -1]])

        self.gridHeight = gridHeight
        self.gridWidth = gridWidth
        self.lockPickProb = lockPickProb
        self.terminalReward = terminalReward


    def isStateTerminal(self, state):
        if state == (3, 0) :
            return True
        elif state == (5, 3):
            return True
        return False

    def takeAction(self, state, action):
        retVal = []
        if(self.isStateTerminal(state)):
            return [[state,1, self.terminalReward]] 

        if action=='left':
            reward = self.rewardsLeft[state]
            if(reward == -1):
                retVal.append([state,1,-1])
            elif(reward == -10):
                retVal.append([(state[0], state[1]-1),self.lockPickProb,-1])
                retVal.append([state,1-self.lockPickProb,-1])
            else:
                retVal.append([(state[0], state[1]-1),1,-1])

        if action=='right':
            reward = self.rewardsRight[state]
            if(reward == -1):
                retVal.append([state,1,-1])
            elif(reward == -10):
                retVal.append([(state[0], state[1]+1),self.lockPickProb,-1])
                retVal.append([state,1-self.lockPickProb,-1])
            else:
                retVal.append([(state[0], state[1]+1),1,-1])

        if action=='up':
            reward = self.rewardsUp[state]
            if(reward == -1):
                retVal.append([state,1,-1])
            elif(reward == -10):
                retVal.append([(state[0]-1, state[1]),self.lockPickProb,-1])
                retVal.append([state,1-self.lockPickProb,-1])
            else:
                retVal.append([(state[0]-1, state[1]),1,-1])

        if action=='down':
            reward = self.rewardsDown[state]
            if(reward == -1):
                retVal.append([state,1,-1])
            elif(reward == -10):
                retVal.append([(state[0]+1, state[1]),self.lockPickProb,-1])
                retVal.append([state,1-self.lockPickProb,-1])
            else:
                retVal.append([(state[0]+1, state[1]),1,-1])
        for i,[nextState, prob, reward] in enumerate(retVal):
            if(self.isStateTerminal(nextState)):
                retVal[i][2] = self.terminalReward   

        return retVal 

class GridworldSolution:
    def __init__(self, maze,horizonLength):
        self.env = maze
        self.actionSpace = ['left', 'right', 'up',  'down']
        self.horizonLength = horizonLength
        self.DP = np.ones((self.env.gridHeight,self.env.gridWidth,self.horizonLength),dtype = float) * -np.inf
    
    def optimalReward(self, state, k):
        optReward =-np.inf
        
    #### Write your code here
      
        if k<self.horizonLength and (maze.isStateTerminal(state))==False:
            for i in solution.actionSpace:
                A=maze.takeAction(state,i)
                if len(A)==1:
                    nextstate,reward=A[0][0],A[0][2]
                    value=reward+self.optimalReward(nextstate,k+1)
                else:
                    nextstate1,nextstate2,p=A[0][0],A[1][0],A[0][1]
                    value=p*(A[0][2]+self.optimalReward(nextstate1,k+1))+(1-p)*(A[1][2]+self.optimalReward(nextstate2,k+1))
                
                if value>optReward:
                    optReward=value
            return optReward
          
        
        if  k<self.horizonLength and (maze.isStateTerminal(state))==True:
                return maze.terminalReward*(self.horizonLength - k )
        if k==self.horizonLength:
                 return 0
       
 ########
     
if __name__ == "__main__":
    maze = Maze()
    solution = GridworldSolution(maze,horizonLength=5)
    print(" Horizon ",solution.horizonLength)
    optReward = solution.optimalReward((2,0),0)
    print(optReward)
    assert optReward==28.0, 'wrong answer'