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
        self.__grabbed = False
        self.__shooted = True
        self.__actions = list()
        self.__traveledplace = [(0, 0)]
        self.__myDirection  = (1, 0)
        self.__myPosition  = (0, 0)
        self.__wallheight = 8
        self.__wallwidth = 5
        self.__wumpusdead = False

    #Return available cells around current
    def adjacentCellsBefore(self, stench, breeze):
        cells = list()
        if stench or breeze:
            return cells
        x, y = self.__myPosition
        if x - 1 >= 0 and ((x-1, y) not in self.__traveledplace):
            cells.append((x-1, y))
        if x + 1 <= self.__wallwidth and ((x+1, y) not in self.__traveledplace):
            cells.append((x+1, y))
        if y - 1 >= 0 and (x, y-1) not in self.__traveledplace:
            cells.append((x, y-1))
        if y + 1 <= self.__wallheight and ((x, y+1) not in self.__traveledplace):
            cells.append((x, y+1))
        return cells

    def adjacentCellsAfter(self, breeze):
        cells = list()
        if breeze:
            return cells
        x, y = self.__myPosition
        if x - 1 >= 0 and (x-1, y) not in self.__traveledplace:
            cells.append((x-1, y))
        if x + 1 <= self.__wallwidth and ((x+1, y) not in self.__traveledplace):
            cells.append((x+1, y))
        if y - 1 >= 0 and (x, y-1) not in self.__traveledplace:
            cells.append((x, y-1))
        if y + 1 <= self.__wallheight and ((x, y+1) not in self.__traveledplace):
            cells.append((x, y+1))
        return cells

    def Move(self, nextposition):
        tgt_dir = (nextposition[0]-self.__myPosition[0], nextposition[1]-self.__myPosition[1])
        if tgt_dir == self.__myDirection:
            if nextposition in self.__actions:
                self.__myPosition = nextposition
                self.__actions.pop()
            else:
                self.__actions.append(self.__myPosition)
                self.__myPosition = nextposition
                self.__traveledplace.append(nextposition)
            return Agent.Action.FORWARD

        elif tgt_dir[0] == self.__myDirection[0] or tgt_dir[1] == self.__myDirection[1]:
            if self.__myDirection[0] == 0:
                self.__myDirection = (-1*self.__myDirection[1], 0)
                return Agent.Action.TURN_LEFT
            elif self.__myDirection[1] == 0:
                self.__myDirection = (0, self.__myDirection[0])
                return Agent.Action.TURN_LEFT
        else:
            if self.__myDirection[0] == 0 and self.__myDirection[1] == tgt_dir[0]:
                self.__myDirection = tgt_dir
                return Agent.Action.TURN_RIGHT
            elif self.__myDirection[0] == 0 and self.__myDirection[1] != tgt_dir[0]:
                self.__myDirection = tgt_dir
                return Agent.Action.TURN_LEFT
            elif self.__myDirection[1] == 0 and self.__myDirection[0] == tgt_dir[1]:
                self.__myDirection = tgt_dir
                return Agent.Action.TURN_LEFT
            elif self.__myDirection[1] == 0 and self.__myDirection[0] != tgt_dir[1]:
                self.__myDirection = tgt_dir
                return Agent.Action.TURN_RIGHT

    def getAction(self, stench, breeze, glitter, bump, scream):
        #print(stench, breeze, glitter, bump)

        if bump:
            if self.__myDirection == (1, 0):
                self.__myPosition = (self.__myPosition[0] - 1, self.__myPosition[1])
                self.__wallwidth = self.__myPosition[0]              
            if self.__myDirection == (0, 1):
                self.__myPosition = (self.__myPosition[0], self.__myPosition[1] - 1)
                self.__wallheight = self.__myPosition[1]
            self.__actions.pop()
        
        # if there is gold, grab it 
        if glitter:
            self.__grabbed = True
            return Agent.Action.GRAB

        ##stench condition 
        if stench and self.__shooted:
            self.__shooted = False
            return Agent.Action.SHOOT
        
        if scream or self.__wumpusdead:
            self.__wumpusdead = True
            Possiblemoves = self.adjacentCellsAfter(breeze)
        else:
            Possiblemoves = self.adjacentCellsBefore(stench,breeze)

        
        # if grabbed, then return to start
        if self.__grabbed:
            ## if actions stack is empty, then climb out
            if self.__actions == list():
                return Agent.Action.CLIMB
            return self.Move(self.__actions[-1])

        # if no adj, then return to start
        if Possiblemoves == list():
            if self.__actions == list():
                return Agent.Action.CLIMB
            return self.Move(self.__actions[-1])
        
        return self.Move(Possiblemoves[0])
