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
        self.__Maps = [[(1000, 0, 0) for k in range(5)] for i in range(8) ] ##0 means unknown, first is heruistic value, sec is pit, third is wumpus
        self.__myPosition = (0,0)
        self.__myDirection = 1 ##0 is up, 1 is right, 2 is down, 3 is left
        self.__traveledplace = list()
        self.__walls = list()
        self.__timesInStart = 0
        self.__Fplace = list()
        self.__lastspot = (-1,-1)
        self.__shootPlaces = list()

        for i in range(8):
            self.__walls.append((i,-1))
        for i in range(5):
            self.__walls.append((-1,i))   
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        #print(stench, breeze, glitter, bump)
        #print(self.__shooted)
        #print(self.__lastspot)
        #print(self.__myPosition)
            
        if (self.__myPosition == (0,0)) and (breeze == True):
            return Agent.Action.CLIMB
        
        if bump:
            self.__actions.pop()
            self.__myPosition = self.__lastspot
            spot = MyAI.nextForwardPosition(self)
            MyAI.WallsAdded(self,spot)
            
        self.__traveledplace.append(self.__myPosition)

        self.__Maps[self.__myPosition[0]][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]][0]-1,self.__Maps[self.__myPosition[0]][self.__myPosition[1]][1],self.__Maps[self.__myPosition[0]][self.__myPosition[1]][2])

        if self.__myPosition == (0,0):
            self.__timesInStart += 1
        if self.__timesInStart >= 4:
            return Agent.Action.CLIMB

        ##breeze condition
        if breeze:
            if (self.__lastspot != self.__myPosition):
                MyAI.changeBreezeValue(self)
        else:
            MyAI.UpdateBreeze(self)

        ##stench condition    
        if stench:
            nextspot = MyAI.nextForwardPosition(self)
            if (self.__shooted == False) and (nextspot not in self.__walls):
                self.__shooted = True
                MyAI.UpdateShootFlag(self)
                return Agent.Action.SHOOT
            if (self.__lastspot != self.__myPosition):
                MyAI.changeStenchValue(self)
        else:
            MyAI.UpdateStunch(self)
        
        # if there is gold, grab it and add it to the actions stack
        if glitter:
            self.__grabbed = True
            self.__actions.append(Agent.Action.GRAB)
            return Agent.Action.GRAB

        for position in self.__traveledplace:
            if self.__traveledplace.count(position) >= 15:
                self.__grabbed = True
                
        
        # if not grabbed, calculate next move
        if not self.__grabbed:
            Possiblemoves = MyAI.getPossibleMoves(self)
            #print(Possiblemoves)
            NextBestSpot = sorted(Possiblemoves, key = lambda x: self.__Maps[x[0]][x[1]][0], reverse = True)[0]
            if MyAI.nextForwardPosition(self) == NextBestSpot:
                self.__actions.append(Agent.Action.FORWARD)
                self.__lastspot = self.__myPosition
                self.__myPosition = NextBestSpot
                return Agent.Action.FORWARD
            elif MyAI.nextRightPosition(self) == NextBestSpot:
                self.__myDirection = (self.__myDirection + 1) % 4
                self.__actions.append(Agent.Action.TURN_RIGHT)
                self.__lastspot = self.__myPosition
                return Agent.Action.TURN_RIGHT
            else:
                self.__myDirection = (self.__myDirection + 3 ) % 4
                self.__actions.append(Agent.Action.TURN_LEFT)
                self.__lastspot = self.__myPosition
                return Agent.Action.TURN_LEFT
        
        # if grabbed, then return to start
        if self.__grabbed:
            if self.__myPosition == (0,0):
                return Agent.Action.CLIMB
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
            if (row,col+1) not in self.__Fplace:
                moves.append((row,col+1))
        elif (col>0 and col<3):
            if (row,col+1) not in self.__Fplace:
                moves.append((row,col+1))
            if (row,col-1) not in self.__Fplace:
                moves.append((row,col-1))
        elif (col>=3):
            if (row,col-1) not in self.__Fplace:
                moves.append((row,col-1))
        #row moves
        if (row<=0):
            if (row+1,col) not in self.__Fplace:
                moves.append((row+1,col))
        elif (row>0 and row<7):
            if (row+1,col) not in self.__Fplace:
                moves.append((row+1,col))
            if (row-1,col) not in self.__Fplace:
                moves.append((row-1,col))
        elif (row>=7):
            if (row-1,col) not in self.__Fplace:
                moves.append((row-1,col))
        final = list()
        for i in moves:
            ##if flag breeze is false then append it
            if (self.__Maps[i[0]][i[1]][1] == False):
                final.append(i)
            if (self.__Maps[i[0]][i[1]][1] == True) and (i in self.__traveledplace):
                final.append(i)

        finalmoves = list()
        for i in final:
            if (self.__Maps[i[0]][i[1]][2] == False):
                finalmoves.append(i)
            if (self.__Maps[i[0]][i[1]][2] == True) and ((i in self.__shootPlaces) or (i in self.__traveledplace)):
                finalmoves.append(i)
                
        last = list()
        for i in finalmoves:
            if i not in self.__walls:
                last.append(i)
        return last

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
        ##when face forward
        if self.__myDirection == 0:
            self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][0],True,self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][2])
            if self.__myPosition[1] <= 0:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][0],True,self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][2])
            if self.__myPosition[1] >= 3:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][0],True,self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][2])
            if self.__myPosition[1] > 0 and self.__myPosition[1] < 3:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][0],True,self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][2])
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][0],True,self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][2])

        ##when face right    
        elif self.__myDirection == 1:
            self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][0],True,self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][2])
            if self.__myPosition[0] <= 0:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][0],True,self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][2])
            if self.__myPosition[0] >= 6:
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][0],True,self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][2])
            if self.__myPosition[0] > 0 and self.__myPosition[0] < 6:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][0],True,self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][2])
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][0],True,self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][2])

        ##when face down         
        elif self.__myDirection == 2:
            if self.__myPosition[0]>= 1:
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][0],True,self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][2])
            if self.__myPosition[1] <= 0:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][0],True,self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][2])
            if self.__myPosition[1] > 0:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][0],True,self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][2])
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][0],True,self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][2])

        ##when face left          
        elif self.__myDirection == 3:
            if self.__myPosition[1]>= 1:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][0],True,self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][2])
            if self.__myPosition[0] <= 0:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][0],True,self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][2])
            if self.__myPosition[0] > 0:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][0],True,self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][2])
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][0],True,self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][2])

        #self.__Fplace = [i for i in self.__Fplace if i not in self.__traveledplace]
        

    def changeStenchValue(self):
        ##when face forward
        if self.__myDirection == 0:
            self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][0],self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][1],True)
            if self.__myPosition[1] <= 0:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][0],self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][1],True)
            if self.__myPosition[1] >= 3:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][0],self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][1],True)
            if self.__myPosition[1] > 0 and self.__myPosition[1] < 3:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][0],self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][1],True)
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][0],self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][1],True)

        ##when face right     
        elif self.__myDirection == 1:
            self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][0],self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][1],True)
            if self.__myPosition[0] <= 0:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][0],self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][1],True)
            if self.__myPosition[0] > 0:
                self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][0],self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][1],True)
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][0],self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][1],True)

        ##when face down         
        elif self.__myDirection == 2:
            self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][0],self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][1],True)
            if self.__myPosition[0]>= 1:
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][0],self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][1],True)
            if self.__myPosition[1] > 0:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][0],self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][1],True)

        ##when face left          
        elif self.__myDirection == 3:
            self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][0],self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][1],True)
            if self.__myPosition[1]>= 1:
                self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][0],self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][1],True)
            if self.__myPosition[0] > 0:
                self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][0],self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][1],True)



    #cleanBreezeFlag
    def UpdateBreeze(self):
        if self.__myPosition[0]== 0:
            self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][0],False,self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][2])
        else:
            self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][0],False,self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][2])
            self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][0],False,self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][2])

        if self.__myPosition[1]== 0:
            self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][0],False,self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][2])
        else:
            self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][0],False,self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][2])
            self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][0],False,self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][2])

    #cleanStunchFlag
    def UpdateStunch(self):
        if self.__myPosition[0]== 0:
            self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][0],self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][1],False)
        else:
            self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][0],self.__Maps[self.__myPosition[0]+1][self.__myPosition[1]][1],False)
            self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]] = (self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][0],self.__Maps[self.__myPosition[0]-1][self.__myPosition[1]][1],False)

        if self.__myPosition[1]== 0:
            self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][0],self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][1],False)
        else:
            self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][0],self.__Maps[self.__myPosition[0]][self.__myPosition[1]+1][1],False)
            self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1] = (self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][0],self.__Maps[self.__myPosition[0]][self.__myPosition[1]-1][1],False)

    def UpdateShootFlag(self):
        
        x = self.__myPosition[0]
        y = self.__myPosition[1]
        ##when face forward
        if self.__myDirection == 0:
            for i in range(x,7):
                self.__shootPlaces.append((i+1,y))

        ##when face right     
        elif self.__myDirection == 1:
            for i in range(y,5):
                self.__shootPlaces.append((x,i+1))

        ##when face down         
        elif self.__myDirection == 2:
            for i in range(0,x):
                self.__shootPlaces.append((i,y))

        ##when face left          
        elif self.__myDirection == 3:
            for i in range(0,y):
                self.__shootPlaces.append((x,i))

    def WallsAdded(self,spot):
        x = spot[0]
        y = spot[1]
        ##when face forward
        if self.__myDirection == 0:
            for i in range(5):
                self.__walls.append((x,i))


        ##when face right     
        elif self.__myDirection == 1:
            for i in range(8):
                self.__walls.append((i,y))

    
    def p(self):
        print(self.__newMaps)

    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
