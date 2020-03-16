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
        self.__actions = list()
        self.__traveledplace = [(0, 0)]
        self.__myDirection  = (1, 0)
        self.__myPosition  = (0, 0)
        self.__wumpusdead = False
        self.__wallheight = 1000
        self.__wallwidth = 1000
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
            self.__actions.pop()
            curr_dir = self.__myDirection
            loc = self.__myPosition
            if curr_dir == (1, 0):
                self.__wallwidth = loc[0] - 1
                self.__myPosition = (loc[0] - 1, loc[1])
            elif curr_dir == (0, 1):
                self.__wallheight = loc[1] - 1
                self.__myPosition = (loc[0], loc[1] - 1)

        ##stench condition 
        if stench and self.__shooted == True:
            self.__shooted = False
            return Agent.Action.SHOOT
        
        if scream or self.__wumpusdead:
            self.__wumpusdead = True
            adj_cells = self.adjacentCellsAfter(breeze)
        
        else:
            adj_cells = self.adjacentCellsBefore(stench,breeze)


        # if grabbed, then return to start
        if self.__grabbed:
            ## if actions stack is empty, then climb out
            if self.__actions == list():
                return Agent.Action.CLIMB
            return self.Move(self.__actions[-1])

        # if no adj, then return to start
        if adj_cells == list():
            if self.__actions == list():
                return Agent.Action.CLIMB
            return self.Move(self.__actions[-1])
        
        return self.Move(adj_cells[0])

    
    #Return available cells around current
    def adjacentCellsBefore(self, stench, breeze):
        cells = list()
        if stench or breeze:
            return cells
        x, y = self.__myPosition
        if self.__myPosition[0] >= 1 and ((x-1, y) not in self.__traveledplace):
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
        TargetDirection = (nextposition[0]-self.__myPosition[0], nextposition[1]-self.__myPosition[1])
        if TargetDirection == self.__myDirection:
            if nextposition in self.__actions:
                self.__myPosition = nextposition
                self.__actions.pop()
            else:
                self.__actions.append(self.__myPosition)
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
            

    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
