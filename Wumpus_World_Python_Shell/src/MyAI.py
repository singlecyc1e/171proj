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
        self.__test = True
        self.__shooted = false
        pass
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        return Agent.Action.CLIMB
        print(self.__actions)
        
        #only for test
        if self.__test:
            self.__test = False
            self.__grabbed = True
            self.__actions.append(Agent.Action.FORWARD)
            return Agent.Action.FORWARD

        # if there is gold, grab it and add it to the actions stack
        if glitter:
            self.__grabbed = True
            self.__actions.append(Agent.Action.GRAB)
            return Agent.Action.GRAB
        
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
                
                self.__actions.append(lastAction)
                self.__turningCounter += 1
                return Agent.Action.TURN_LEFT
            print("??")
        
        return Agent.Action.CLIMB
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================

    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
