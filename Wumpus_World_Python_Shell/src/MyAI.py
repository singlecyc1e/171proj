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


class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.__grabbed = False
        self.__actions = list()
        self.__turnedHEAD = False
        self.__turningCounter = 0
        self.__shooted = False
        self.__Maps = [[1000 for k in range(5)] for i in range(8) ]
        self.__Maps[0][0] = 0
        self.__myPosition = (0,0)
        self.__myDirection = 1 ##0 is up, 1 is right, 2 is down, 3 is left
        self.__traveledplace = list()
        self.__walls = list()
        self.__breezeplaces = list()
        self.__stenchplaces = list()
        self.__timesInStart = 0
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        print(stench, breeze, glitter, bump)
        if (scream) and (not breeze):
            nextmove = MyAI.nextForwardPosition(self)
            self.__Maps[nextmove[0]][nextmove[1]] = 1000
            
        if (self.__myPosition == (0,0)) and (breeze == True):
            return Agent.Action.CLIMB

        if (self.__myPosition == (0,0) )and (stench) and (not self.__shooted ):
            self.__shooted = True
            return Agent.Action.SHOOT
        
        if bump:
            self.__actions.pop()
            self.__myPosition = self.__lastspot
            spot = MyAI.nextForwardPosition(self)
            self.__walls.append(spot)

        self.__traveledplace.append(self.__myPosition)

        self.__Maps[self.__myPosition[0]][self.__myPosition[1]] = 0

        if self.__myPosition == (0,0):
            self.__timesInStart += 1
        if self.__timesInStart >= 9:
            return Agent.Action.CLIMB
            
        if breeze:
            MyAI.changeBreezeValue(self)
            self.__breezeplaces.append((self.__myPosition[0],self.__myPosition[1]))
            
        if stench:
            MyAI.changeStenchValue(self)
            self.__stenchplaces.append((self.__myPosition[0],self.__myPosition[1]))
        

            
        if (not bump) and (not stench)and (not breeze):
            MyAI.changeEmptyValue(self)

        for i in self.__traveledplace:
            self.__Maps[i[0]][i[1]] = 0

        if(self.__walls != list()):
            for i in self.__walls:
                self.__Maps[i[0]][i[1]] = -10000

        if(self.__breezeplaces != list()):
            for i in self.__breezeplaces:
                self.__Maps[i[0]][i[1]] = -2000

        if(self.__stenchplaces != list()):
            for i in self.__stenchplaces:
                self.__Maps[i[0]][i[1]] = -5000
    
        print(self.__myPosition)
        print(self.__grabbed)
        
        # if there is gold, grab it and add it to the actions stack
        if glitter:
            self.__grabbed = True
            self.__actions.append(Agent.Action.GRAB)
            return Agent.Action.GRAB

        # if not grabbed, calculate next move
        if not self.__grabbed:
            Possiblemoves = MyAI.getPossibleMoves(self)
            NextBestSpot = sorted(Possiblemoves, key = lambda x: self.__Maps[x[0]][x[1]], reverse = True)[0]
            if MyAI.nextForwardPosition(self) == NextBestSpot:
                self.__actions.append(Agent.Action.FORWARD)
                self.__lastspot = self.__myPosition
                self.__myPosition = NextBestSpot
                return Agent.Action.FORWARD
            elif MyAI.nextRightPosition(self) == NextBestSpot:
                self.__myDirection = (self.__myDirection + 1) % 4
                self.__actions.append(Agent.Action.TURN_RIGHT)
                return Agent.Action.TURN_RIGHT
            else:
                self.__myDirection = (self.__myDirection + 3 ) % 4
                self.__actions.append(Agent.Action.TURN_LEFT)
                return Agent.Action.TURN_LEFT
        
        # if grabbed, then return to start
        if self.__grabbed:
            
            ## if actions stack is empty, then climb out
            if self.__actions == list():
                return Agent.Action.CLIMB

            ## check what is the last action
            lastAction = self.__actions.pop()

            if lastAction == Agent.Action.FORWARD:
                if self.__turnedHEAD:
                    return lastAction
                
                if self.__turningCounter == 1:
                    self.__turnedHEAD = True
                    self.__turningCounter = 0
                    self.__actions.append(lastAction)
                    return Agent.Action.TURN_LEFT
                
                self.__myDirection = (self.__myDirection + 3 ) % 4
                self.__actions.append(lastAction)
                self.__turningCounter += 1
                
                return Agent.Action.TURN_LEFT

            if lastAction == Agent.Action.TURN_LEFT:
                self.__myDirection = (self.__myDirection + 1 ) % 4
                return Agent.Action.TURN_RIGHT

            if lastAction == Agent.Action.TURN_RIGHT:
                self.__myDirection = (self.__myDirection + 3 ) % 4
                return Agent.Action.TURN_LEFT
        
        return Agent.Action.CLIMB
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def getPossibleMoves(self):
        moves = list()
        row = self.__myPosition[0]
        col = self.__myPosition[1]
        ##col moves
        if (col<=0):
            moves.append((row,col+1))
        elif (col>0 and col<3):
            moves.append((row,col+1))
            moves.append((row,col-1))
        elif (col>=3):
            moves.append((row,col-1))
        #row moves
        if (row<=0):
            moves.append((row+1,col))
        elif (row>0 and row<7):
            moves.append((row+1,col))
            moves.append((row-1,col))
        elif (row>=7):
            moves.append((row-1,col))
            
        return moves

    def nextForwardPosition(self):
        if self.__myDirection == 0:
            return (self.__myPosition[0]+1,self.__myPosition[1])
        if self.__myDirection == 1:
            return (self.__myPosition[0],self.__myPosition[1]+1)
        if self.__myDirection == 2:
            return (self.__myPosition[0]-1,self.__myPosition[1])
        if self.__myDirection == 3:
            return (self.__myPosition[0],self.__myPosition[1]-1)

    def nextRightPosition(self):
        if self.__myDirection == 0:
            return (self.__myPosition[0],self.__myPosition[1]+1)
        if self.__myDirection == 1:
            return (self.__myPosition[0]-1,self.__myPosition[1])
        if self.__myDirection == 2:
            return (self.__myPosition[0],self.__myPosition[1]-1)
        if self.__myDirection == 3:
            return (self.__myPosition[0]+1,self.__myPosition[1])

    def changeBreezeValue(self):
        if self.__myDirection == 0:
            if self.__myPosition[0]<= 5:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] -= 2000
            if self.__myPosition[1] <= 0:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] -= 2000
            if self.__myPosition[1] >= 3:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] -= 2000
            if self.__myPosition[1] > 0 and self.__myPosition[1] < 3:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] -= 2000
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] -= 2000
            
        elif self.__myDirection == 1:
            if self.__myPosition[1]<= 2:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] -= 2000
            if self.__myPosition[0] <= 0:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] -= 2000
            if self.__myPosition[0] >= 6:
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] -= 2000
            if self.__myPosition[0] > 0 and self.__myPosition[0] < 6:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] -= 2000
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] -= 2000
                
        elif self.__myDirection == 2:
            if self.__myPosition[0]>= 1:
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] -= 2000
            if self.__myPosition[1] <= 0:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] -= 2000
            if self.__myPosition[1] >= 3:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] -= 2000
            if self.__myPosition[1] > 0 and self.__myPosition[1] < 3:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] -= 2000
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] -= 2000
                
        elif self.__myDirection == 3:
            if self.__myPosition[1]>= 1:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] -= 2000
            if self.__myPosition[0] <= 0:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] -= 2000
            if self.__myPosition[0] >= 6:
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] -= 2000
            if self.__myPosition[0] > 0 and self.__myPosition[0] < 6:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] -= 2000
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] -= 2000

    def changeStenchValue(self):
        if self.__myDirection == 0:
            if self.__myPosition[0]<= 5:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] -= 1500
            if self.__myPosition[1] <= 0:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] -= 1500
            if self.__myPosition[1] >= 3:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] -= 1500
            if self.__myPosition[1] > 0 and self.__myPosition[1] < 3:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] -= 1500
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] -= 1500
            
        elif self.__myDirection == 1:
            if self.__myPosition[1]<= 2:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] -= 1500
            if self.__myPosition[0] <= 0:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] -= 1500
            if self.__myPosition[0] >= 6:
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] -= 1500
            if self.__myPosition[0] > 0 and self.__myPosition[0] < 6:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] -= 1500
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] -= 1500
                
        elif self.__myDirection == 2:
            if self.__myPosition[0]>= 1:
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] -= 1500
            if self.__myPosition[1] <= 0:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] -= 1500
            if self.__myPosition[1] >= 3:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] -= 1500
            if self.__myPosition[1] > 0 and self.__myPosition[1] < 3:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] -= 1500
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] -= 1500
                
        elif self.__myDirection == 3:
            if self.__myPosition[1]>= 1:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] -= 1500
            if self.__myPosition[0] <= 0:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] -= 1500
            if self.__myPosition[0] >= 6:
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] -= 1500
            if self.__myPosition[0] > 0 and self.__myPosition[0] < 6:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] -= 1500
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] -= 1500

    def changeEmptyValue(self):
        if self.__myDirection == 0:
            if self.__myPosition[0]<= 5:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = 1000
            if self.__myPosition[1] <= 0:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = 1000
            if self.__myPosition[1] >= 3:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] = 1000
            if self.__myPosition[1] > 0 and self.__myPosition[1] < 3:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = 1000
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] = 1000
            
        elif self.__myDirection == 1:
            if self.__myPosition[1]<= 2:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = 1000
            if self.__myPosition[0] <= 0:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = 1000
            if self.__myPosition[0] >= 6:
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] = 1000
            if self.__myPosition[0] > 0 and self.__myPosition[0] < 6:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = 1000
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] = 1000
            
        elif self.__myDirection == 2:
            if self.__myPosition[0]>= 1:
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] = 1000
            if self.__myPosition[1] <= 0:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = 1000
            if self.__myPosition[1] >= 3:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] = 1000
            if self.__myPosition[1] > 0 and self.__myPosition[1] < 3:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = 1000
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] = 1000
                
        elif self.__myDirection == 3:
            if self.__myPosition[1]>= 1:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] = 1000
            if self.__myPosition[0] <= 0:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = 1000
            if self.__myPosition[0] >= 6:
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] = 1000
            if self.__myPosition[0] > 0 and self.__myPosition[0] < 6:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = 1000
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] = 1000

    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
