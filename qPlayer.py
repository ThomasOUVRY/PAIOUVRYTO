import random
import matplotlib.pyplot as plt
import game421

keep = "keep"
roll = "roll"


class QPlayer(game421.AbsAgent):
    def __init__(self, explorationRatio=0.1, discountFactor=0.99, learningRate=0.1):
        super().__init__()
        self.score = 0
        self.explorationRatio = explorationRatio  # the exploration ratio, 0.1 over 1 chance to take a random action.
        self.discountFactor = discountFactor  # the discount factors, interest of immediate reward regarding future gains
        self.learningRate = learningRate  # the learning rate, speed that incoming experiences erase the oldest.
        self.qvalues = {}  # dictionnaire de valeur

    # Agent interfase:
    def wakeUp(self, initialState, stateDsc, actionSpace):
        # Reccord initial state:
        self.state = initialState
        # Reccord the list of all possible actions:
        self.actions = actionSpace
        # Initialize a new state in Q if necessary:
        self.init_row_for_state(self.state)

    def init_row_for_state(self, state):
        if state not in self.qvalues.keys():
            self.qvalues[state] = {a: 0.0 for a in self.actions}

    # find the next action
    def decide(self, isValidAction):
        if random.uniform(0, 1) < self.explorationRatio:  # explore
            self.action = self.random_action()
        else:  # play the best move
            self.action = self.find_best_action(self.stateStr())
        return self.action

    def random_action(self):
        decision_list = []
        for diceIdx in range(0, 3):
            explore_decide_keep: bool = random.choice([True, False])
            if explore_decide_keep:
                decision_list.append(keep)
            else:
                decision_list.append(roll)
        return '-'.join(decision_list)

    # maximasing Q(s,a)
    def find_best_action(self, state):
        best_action = '-'.join([roll, roll, roll])
        curr_state = state
        for i in self.qvalues[curr_state]:
            if self.qvalues[curr_state][i] > self.qvalues[curr_state][best_action]:
                best_action = i
        return best_action

    #
    def perceive(self, reachedStateStr, reward):
        self.init_row_for_state(reachedStateStr)
        self.qUpdate(reachedStateStr, reward)
        self.state = reachedStateStr

    def qUpdate(self, reachedState, reward):
        oldValue = self.qvalues[self.state][self.action]
        currentValue = self.qvalues[reachedState][self.find_best_action(reachedState)]
        self.qvalues[self.state][self.action] = (1 - self.learningRate) * oldValue + self.learningRate * (
                reward + self.discountFactor * currentValue)


def main():
    player = QPlayer(explorationRatio=0.1, learningRate=0.01)
    games = 100
    rerolls = 1000
    gameEngine = game421.System()
    stats = {"exploration": [], "average score": [], "average best Q": []}
    for v in range(rerolls):
        total = 0
        # Perfrom `samples` games, by reccording the reached score:
        for i in range(games):
            gameEngine.run(player)
            total += player.score
        # Annalyse the qvalue object after `samples` games:
        # Record exploration indicator: the number of visited states:
        sizeQ = len(player.qvalues)
        stats["exploration"].append(sizeQ)
        # Record the average score:
        sumQ = 0
        for s in player.qvalues:
            aStar = player.find_best_action(s)
            sumQ += player.qvalues[s][aStar]
        stats["average score"].append(total / games)
        # Record the average best Q value for each state:
        stats["average best Q"].append(sumQ / sizeQ)

    for elt in stats:
        plt.plot(stats[elt])
        plt.ylabel(elt)
        plt.show()


# Activate default interface :
if __name__ == '__main__':
    main()
