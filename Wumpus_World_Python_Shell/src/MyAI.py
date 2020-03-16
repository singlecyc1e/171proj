# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent


class MyAI (Agent):

    def __init__(self):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.__grabbed = False
        self.__shooted = False
        self.__myDirection  = (1, 0) ## self.__myDirection  = 1 
        self.__myPosition  = (0, 0)
        self.__wumpusdead = False
        self.__wallheight = 9
        self.__wallwidth = 6
        self.__placesStack = list()
        self.__traveledplace = [(0, 0)]
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================


    def getAction(self, stench, breeze, glitter, bump, scream):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        #print(stench, breeze, glitter, bump)
        
        # if there is gold, grab it 
        if glitter:
            self.__grabbed = True
            return Agent.Action.GRAB

        if stench and not self.__shooted:
            self.__shooted = True
            return Agent.Action.SHOOT

        if bump:
            ##when face forward
            if self.__myDirection == (0, 1): ##self.__myDirection == 0
                self.__myPosition = (self.__myPosition[0], self.__myPosition[1]-1)
                self.__wallheight = self.__myPosition[1]
                
            ##when face right
            if self.__myDirection == (1, 0): ##self.__myDirection == 1
                self.__myPosition = (self.__myPosition[0]-1, self.__myPosition[1])
                self.__wallwidth = self.__myPosition[0]
                  
            self.__placesStack.pop()

        if scream:
            self.__wumpusdead = True
        
        Possiblemoves = self.getPossibleMoves(stench,breeze)
        
        # if grabbed, then return to start
        if self.__grabbed:
            ## if place stack is empty, then climb out
            if self.__placesStack == list():
                return Agent.Action.CLIMB
            
            Action = self.Back(self.__placesStack[-1])
            return Action

        # if no adj, then return to start
        if Possiblemoves == list():
            if self.__placesStack == list():
                return Agent.Action.CLIMB
            
            Action = self.Back(self.__placesStack[-1])
            return Action
        
        Action = self.Move(Possiblemoves[0])
        return Action


        #Return available cells around current
    def getPossibleMoves(self, stench, breeze):
        moves = list()
        if self.__wumpusdead:
            if breeze:
                return moves
        else:
            if stench or breeze:
                return moves

        if self.__myPosition[0] > 0:
            moves.append((self.__myPosition[0]-1, self.__myPosition[1]))
        if self.__myPosition[0] < self.__wallwidth:
            moves.append((self.__myPosition[0]+1, self.__myPosition[1]))
        if self.__myPosition[1] > 0:
            moves.append((self.__myPosition[0], self.__myPosition[1]-1))
        if self.__myPosition[1] < self.__wallheight:
            moves.append((self.__myPosition[0], self.__myPosition[1]+1))
            
        final  = list()
        for i in moves:
            if i not in self.__traveledplace:
                final.append(i)
                
        return final
    
    def Back(self, nextposition):
        TargetDirection = (nextposition[0]-self.__myPosition[0], nextposition[1]-self.__myPosition[1])
        if TargetDirection == self.__myDirection:
            self.__myPosition = nextposition
            self.__placesStack.pop()
            return Agent.Action.FORWARD
        
        ##when direction change can achieve by one action
        if TargetDirection[0] != self.__myDirection[0] and TargetDirection[1] != self.__myDirection[1]:

            ##turn right condition
            if self.__myDirection[0] == 0 and self.__myDirection[1] == TargetDirection[0]:
                self.__myDirection = TargetDirection
                return Agent.Action.TURN_RIGHT
            if self.__myDirection[1] == 0 and self.__myDirection[0] != TargetDirection[1]:
                self.__myDirection = TargetDirection
                return Agent.Action.TURN_RIGHT

            ##turn left condition
            if self.__myDirection[0] == 0 and self.__myDirection[1] != TargetDirection[0]:
                self.__myDirection = TargetDirection
                return Agent.Action.TURN_LEFT
            if self.__myDirection[1] == 0 and self.__myDirection[0] == TargetDirection[1]:
                self.__myDirection = TargetDirection
                return Agent.Action.TURN_LEFT

            
        ##when direction change can achieve by two action
        else:
            if self.__myDirection[0] == 0:
                self.__myDirection = (self.__myDirection[1] * -1, 0)
            elif self.__myDirection[1] == 0:
                self.__myDirection = (0, self.__myDirection[0])

            return Agent.Action.TURN_RIGHT
        

    def Move(self, nextposition):
        TargetDirection = (nextposition[0]-self.__myPosition[0], nextposition[1]-self.__myPosition[1])
        
        if TargetDirection == self.__myDirection:
            self.__placesStack.append(self.__myPosition)
            self.__traveledplace.append(nextposition)
            self.__myPosition = nextposition                    
            return Agent.Action.FORWARD

        ##when direction change can achieve by one action
        if TargetDirection[0] != self.__myDirection[0] and TargetDirection[1] != self.__myDirection[1]:
            ##turn right condition
            if self.__myDirection[0] == 0 and self.__myDirection[1] == TargetDirection[0]:
                self.__myDirection = TargetDirection
                return Agent.Action.TURN_RIGHT
            if self.__myDirection[1] == 0 and self.__myDirection[0] != TargetDirection[1]:
                self.__myDirection = TargetDirection
                return Agent.Action.TURN_RIGHT

            ##turn left condition
            if self.__myDirection[0] == 0 and self.__myDirection[1] != TargetDirection[0]:
                self.__myDirection = TargetDirection
                return Agent.Action.TURN_LEFT
            if self.__myDirection[1] == 0 and self.__myDirection[0] == TargetDirection[1]:
                self.__myDirection = TargetDirection
                return Agent.Action.TURN_LEFT
            
        ##when direction change can achieve by two action
        else:
            if self.__myDirection[0] == 0:
                self.__myDirection = (self.__myDirection[1] * -1, 0)
            elif self.__myDirection[1] == 0:
                self.__myDirection = (0, self.__myDirection[0])

            return Agent.Action.TURN_RIGHT
        
            
    def p(self):
        print(self.__traveledplace)
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
