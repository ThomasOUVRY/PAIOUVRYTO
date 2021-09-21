#!env python3
"""
Script 421 GAME - Guillaume Lozenguez
"""
import random


# Default game interface :
def main():
    gameEngine = System()
    player = HumanAgent()
    gameEngine.run(player)


# Agent as a very simple UI
class AbsAgent:

    # Object Methods:
    # ---------------
    def __init__(self, sep="-"):
        self.separator = sep

    # Agent Methods:
    # ---------------

    def wakeUp(self, initialStateStr, stateDsc, actionSpace):
        # I wake up the agent with:
        #  - an initial state,
        #  - a description of state varibles
        #  - the collection of all possible actions
        self.descriptor = stateDsc
        self.state = initialStateStr
        self.score = 0

    def perceive(self, reachedStateStr, reward):
        pass

    def decide(self, isValidAction):
        pass

    def sleep(self, score):
        self.score = score

    # state and action manipulation:
    # -------------------------------

    def stateStr(self):
        return self.state

    def stateVector(self):
        return self.state.split(self.separator)

    def stateDico(self):
        return {k: val for k, val in zip(self.descriptor, self.stateVector())}


class HumanAgent(AbsAgent):

    def wakeUp(self, initialStateStr, stateDsc, actionSpace):
        super().wakeUp(initialStateStr, stateDsc, actionSpace)
        print("Start a new game, possible actions are:")
        print(actionSpace)
        print("Perception: " + initialStateStr)

    def perceive(self, reachedStateStr, reward):
        self.state = reachedStateStr
        print("Perception: " + self.state + " with reward : " + str(reward))

    def decide(self, isValidAction):
        print("Action ?")
        actionStr = ""
        while not isValidAction(actionStr):
            actionStr = input()
        return actionStr

    def sleep(self, score):
        super().sleep(score)
        print("Game end on score: " + str(score))


# Game engine :
class System:

    # Constructor : set a Horizon and initialize the game
    def __init__(self, horizon=3):
        self.horizon = horizon
        self.initialize()

    # Initialize a random first state with a reset horizon counter
    def initialize(self, numberOfPlayers=1):
        dice = self.randomDice([1, 1, 1], ["roll", "roll", "roll"])
        self.state = {"H": self.horizon - 1, "D1": dice[0], "D2": dice[1], "D3": dice[2]}

    # Run : run the engine with a player, until a final state is reached
    # Players as classical Agent that can perceive and respond with actions
    def run(self, player):
        self.initialize()
        player.wakeUp(self.stateStr(), ["Horizon", "D1", "D2", "D3"], self.allActionsStr())
        reward = 0.0
        while not self.isEnd():
            action = player.decide(self.isActionStr)
            reward = self.step(self.actionFromStr(action))
            player.perceive(self.stateStr(), reward)
        player.sleep(reward)

    # Generate a list of all the possible states
    def allStates(self):
        allStates = []
        for h in range(self.horizon):
            for i1 in range(1, 7):
                for i2 in range(1, i1 + 1):
                    for i3 in range(1, i2 + 1):
                        state = {"H": h, "D1": i1, "D2": i2, "D3": i3}
                        allStates.append(state)
        return allStates

    def allStatesStr(self):
        allStatesStr = ['-'.join([str(v) for v in s.values()]) for s in self.allStates()]
        return allStatesStr

    # Generate a list of all the possible actions
    def allActions(self):
        allActions = []
        for i1 in ["keep", "roll"]:
            for i2 in ["keep", "roll"]:
                for i3 in ["keep", "roll"]:
                    action = {"A1": i1, "A2": i2, "A3": i3}
                    allActions.append(action)
        return allActions

    def allActionsStr(self):
        allActions = self.allActions()
        allActionStr = ['-'.join(action.values()) for action in allActions]
        return allActionStr

    # Return the current state as a variable dictionary
    def stateDico(self):
        return self.state

    # set the current state to 'state' (suposed to be a dictionary)
    def setOnStateDico(self, state):
        self.state = state

    # generate a string from the current state
    def stateStr(self):
        return str(self.state["H"]) + "-" + str(self.state["D1"]) + "-" + str(self.state["D2"]) + "-" + str(
            self.state["D3"])

    # Deconpose a string to set the current state
    def setOnStateStr(self, state_str):
        values = [int(x_str) for x_str in state_str.split("-")]
        self.setOnStateDico({"H": values[0], "D1": values[1], "D2": values[2], "D3": values[3]})

    # Return True if the current state match a final state.
    def isEnd(self):
        return self.state["H"] == 0

    # Decompose a string and set the current action accordingly
    def actionFromStr(self, act_str):
        values = act_str.split("-")
        return {"A1": values[0], "A2": values[1], "A3": values[2]}

    # Generate a string from the current action
    def actionToStr(self, act):
        return act["A1"] + "-" + act["A2"] + "-" + act["A3"]

    # Test if a string match a game action
    def isActionStr(self, act_str):
        values = act_str.split("-")
        ok = len(values) == 3
        for a in values:
            if not (a == "keep" or a == "roll"):
                ok = False
        return ok

    # Return the potential score of a game
    def score(self, state):
        if state["D1"] == 4 and state["D2"] == 2 and state["D3"] == 1: # 421
            return 800

        if state["D1"] == 1 and state["D2"] == 1 and state["D3"] == 1: # 111
            return 700

        if state["D2"] == 1 and state["D3"] == 1: # X11
            return 400 + state["D1"]

        if state["D2"] == state["D1"] and state["D3"] == state["D1"]: #XXX
            return 300 + state["D1"]

        if state["D2"] == state["D1"] - 1 and state["D3"] == state["D1"] - 2:
            return 200 + state["D1"]

        if state["D1"] == 2 and state["D2"] == 2 and state["D3"] == 1:
            return 0

        return 100 + state["D1"]

    # Roll the dice accordinglly to the actions
    def randomDice(self, dice, act):
        new_dice = []
        for die, act in zip(dice, act):
            if act == "roll" or act == "r":
                new_dice.append(random.choice(range(1, 7)))
            else:
                new_dice.append(die)
        new_dice.sort(reverse=True)
        return new_dice

    # Generate a random transition
    def randomTransition(self, action):
        if action["A1"] == "keep" and action["A2"] == "keep" and action["A3"] == "keep":
            self.state["H"] = 0
        if self.state["H"] == 0:
            return self.state
        dice = [self.state["D1"], self.state["D2"], self.state["D3"]]
        diceAct = [action["A1"], action["A2"], action["A3"]]
        dice = self.randomDice(dice, diceAct)
        return {"H": self.state["H"] - 1, "D1": dice[0], "D2": dice[1], "D3": dice[2]}

    # Apply the current action to the current state to step forward the engine
    def step(self, action):
        # Get a random transition
        horizon = self.state["H"]
        self.state = self.randomTransition(action)
        # Compute the associated reward
        if horizon != 0 and self.state["H"] == 0:
            return self.score(self.state)
        else:
            return 0.0


# Activate default interface :
if __name__ == '__main__':
    main()