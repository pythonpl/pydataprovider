from enum import Enum
import math

# Machine states enum
class State(Enum):
    OFF = 0
    ON = 1
    STARTING = 2
    STOPPING = 3

# Equations to calculate parameter value
class Equations():
    OFF = "0.0"
    ON = "1.0"
    STARTING = "-(math.e ** (-t)) + 1"
    STOPPING = "math.e ** (-t)"
    invSTARTING = "-math.log(1 - v)"
    invSTOPPING = "-math.log(v)"


# Machine model
# ON/OFF and float parameter return
# Quick and dirty version, but enough for the basic visu simulator
class Model():
    def __init__(self, amp = 1.0):
        self.amp = amp
        self.parameter = 0
        self.timeInState = 0
        self.changed = False
        self.newState = State.OFF
        self.oldState = State.OFF
        self.currentModel = Equations.OFF

    def tick(self):
        self.timeInState += 0.5
        if self.changed:
            if (self.oldState == State.OFF and self.newState == State.STARTING) or (self.oldState == State.ON and self.newState == State.STOPPING):
                self.timeInState = 0
            elif self.newState == State.ON or self.newState == State.OFF:
                self.timeInState = 0
            elif (self.oldState == State.STARTING and self.newState == State.STOPPING):
                v = self.parameter
                self.timeInState = eval(Equations.invSTOPPING)
            elif (self.oldState == State.STOPPING and self.newState == State.STARTING):
                v = self.parameter
                self.timeInState = eval(Equations.invSTARTING)
            self.changed = False
            
            if self.newState == State.STARTING:
                self.currentModel = Equations.STARTING
            if self.newState == State.STOPPING:
                self.currentModel = Equations.STOPPING
            if self.newState == State.ON:
                self.currentModel = Equations.ON
            if self.newState == State.OFF:
                self.currentModel = Equations.OFF
            
            self.oldState = self.newState

        if (abs(self.parameter - 1) < 0.01) and self.newState == State.STARTING:
            self.newState = State.ON
            self.changed = True
        if (abs(self.parameter) < 0.01) and self.newState == State.STOPPING:
            self.newState = State.OFF 

            self.changed = True

        t = self.timeInState
        self.parameter = eval(self.currentModel)

    def getParameter(self):
        return self.parameter * self.amp

    def start(self):
        self.newState = State.STARTING
        self.changed = True

    def stop(self):
        self.newState = State.STOPPING
        self.changed = True

