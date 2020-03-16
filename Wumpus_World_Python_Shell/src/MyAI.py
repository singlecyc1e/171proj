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
        self.upBound = 10000
        self.rightBound = 10000
        
        self.visited = [(0, 0)]
        self.status = {"Direction": (1, 0), "Location": (0, 0)}
        self.__wumpusdead = False

    #Return available cells around current
    def adjacentCellsBefore(self, stench, breeze):
        cells = list()
        if stench or breeze:
            return cells
        x, y = self.status["Location"]
        if x - 1 >= 0 and (x-1, y) not in self.visited:
            cells.append((x-1, y))
        if x + 1 <= self.rightBound and (x+1, y) not in self.visited:
            cells.append((x+1, y))
        if y - 1 >= 0 and (x, y-1) not in self.visited:
            cells.append((x, y-1))
        if y + 1 <= self.upBound and (x, y+1) not in self.visited:
            cells.append((x, y+1))
        return cells

    def adjacentCellsAfter(self, breeze):
        cells = list()
        if breeze:
            return cells
        x, y = self.status["Location"]
        if x - 1 >= 0 and (x-1, y) not in self.visited:
            cells.append((x-1, y))
        if x + 1 <= self.rightBound and (x+1, y) not in self.visited:
            cells.append((x+1, y))
        if y - 1 >= 0 and (x, y-1) not in self.visited:
            cells.append((x, y-1))
        if y + 1 <= self.upBound and (x, y+1) not in self.visited:
            cells.append((x, y+1))
        return cells

    #Set right bound or up bound when perceiving bump
    def setBound(self):
        curr_dir, loc = self.status["Direction"], self.status["Location"]
        if curr_dir == (1, 0):
            self.rightBound = loc[0] - 1
            self.status["Location"] = (loc[0] - 1, loc[1])
        elif curr_dir == (0, 1):
            self.upBound = loc[1] - 1
            self.status["Location"] = (loc[0], loc[1] - 1)

    def toCell(self, nextmove):
        curr_dir, loc = self.status["Direction"], self.status["Location"]
        tgt_dir = (nextmove[0]-loc[0], nextmove[1]-loc[1])

        if tgt_dir == curr_dir:
            if nextmove in self.__actions:
                self.status["Location"] = nextmove
                self.__actions.pop()
            else:
                self.__actions.append(self.status["Location"])
                self.status["Location"] = nextmove
                self.visited.append(nextmove)
            return Agent.Action.FORWARD

        elif tgt_dir[0] == curr_dir[0] or tgt_dir[1] == curr_dir[1]:
            if curr_dir[0] == 0:
                self.status["Direction"] = (-1*curr_dir[1], 0)
                return Agent.Action.TURN_LEFT
            elif curr_dir[1] == 0:
                self.status["Direction"] = (0, curr_dir[0])
                return Agent.Action.TURN_LEFT
        else:
            if curr_dir[0] == 0 and curr_dir[1] == tgt_dir[0]:
                self.status["Direction"] = tgt_dir
                return Agent.Action.TURN_RIGHT
            elif curr_dir[0] == 0 and curr_dir[1] != tgt_dir[0]:
                self.status["Direction"] = tgt_dir
                return Agent.Action.TURN_LEFT
            elif curr_dir[1] == 0 and curr_dir[0] == tgt_dir[1]:
                self.status["Direction"] = tgt_dir
                return Agent.Action.TURN_LEFT
            elif curr_dir[1] == 0 and curr_dir[0] != tgt_dir[1]:
                self.status["Direction"] = tgt_dir
                return Agent.Action.TURN_RIGHT

    def getAction(self, stench, breeze, glitter, bump, scream):
        #print(stench, breeze, glitter, bump)

        if glitter:
            self.__grabbed = True
            return Agent.Action.GRAB

        if bump:
            self.__actions.pop()
            self.setBound()
        
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
            if not self.__actions:
                return Agent.Action.CLIMB
            return self.toCell(self.__actions[-1])

        # if no adj, then return to start
        if adj_cells == list():
            if not self.__actions:
                return Agent.Action.CLIMB
            return self.toCell(self.__actions[-1])
        
        return self.toCell(adj_cells[0])
