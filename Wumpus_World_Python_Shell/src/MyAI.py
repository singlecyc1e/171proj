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
        self.__shooted = True
        self.__places = list()
        self.__traveledplace = [(0, 0)]
        self.__myDirection  = (1, 0)
        self.__myPosition  = (0, 0)
        self.__wumpusdead = False
        self.__wallheight = 10
        self.__wallwidth = 10
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

        if bump:
            self.__places.pop()
            curr_dir = self.__myDirection
            loc = self.__myPosition
            if curr_dir == (1, 0):
                self.__wallwidth = loc[0] - 1
                self.__myPosition = (loc[0] - 1, loc[1])
            elif curr_dir == (0, 1):
                self.__wallheight = loc[1] - 1
                self.__myPosition = (loc[0], loc[1] - 1)

        ##stench condition 
        if stench and self.__shooted:
            self.__shooted = False
            return Agent.Action.SHOOT
        
        if scream or self.__wumpusdead:
            self.__wumpusdead = True
        
        Possiblemoves = self.getPossibleMoves(stench,breeze)

        
        # if grabbed, then return to start
        if self.__grabbed:
            ## if place stack is empty, then climb out
            if self.__places == list():
                return Agent.Action.CLIMB
            return self.Move(self.__places[-1])

        # if no adj, then return to start
        if Possiblemoves == list():
            if self.__places == list():
                return Agent.Action.CLIMB
            return self.Move(self.__places[-1])
        
        return self.Move(Possiblemoves[0])


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

    def Move(self, nextposition):
        TargetDirection = (nextposition[0]-self.__myPosition[0], nextposition[1]-self.__myPosition[1])
        if TargetDirection == self.__myDirection:
            if nextposition in self.__places:
                self.__myPosition = nextposition
                self.__places.pop()
            else:
                self.__places.append(self.__myPosition)
                self.__myPosition = nextposition
                self.__traveledplace.append(nextposition)
            return Agent.Action.FORWARD

        elif TargetDirection[0] == self.__myDirection[0] or TargetDirection[1] == self.__myDirection[1]:
            if self.__myDirection[0] == 0:
                self.__myDirection = (-1*self.__myDirection[1], 0)
                return Agent.Action.TURN_LEFT
            elif self.__myDirection[1] == 0:
                self.__myDirection = (0, self.__myDirection[0])
                return Agent.Action.TURN_LEFT
        else:
            if self.__myDirection[0] == 0 and self.__myDirection[1] == TargetDirection[0]:
                self.__myDirection = TargetDirection
                return Agent.Action.TURN_RIGHT
            elif self.__myDirection[0] == 0 and self.__myDirection[1] != TargetDirection[0]:
                self.__myDirection = TargetDirection
                return Agent.Action.TURN_LEFT
            elif self.__myDirection[1] == 0 and self.__myDirection[0] == TargetDirection[1]:
                self.__myDirection = TargetDirection
                return Agent.Action.TURN_LEFT
            elif self.__myDirection[1] == 0 and self.__myDirection[0] != TargetDirection[1]:
                self.__myDirection = TargetDirection
                return Agent.Action.TURN_RIGHT
            
    def p(self):
        print(self.__traveledplace)
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
