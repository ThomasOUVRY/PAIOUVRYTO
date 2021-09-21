import game421
import json


# Input: an MDP: <S,A,T,R>; precision error: epsilon ; discount factor: gamma ; initial V(s)
# 1. Repeat until the *maximal delta < epsilon
# For each state s in S
# ▬ Search the action a* maximizing the Bellman Equation on s
# ▬ Update pi(s) and V(s) by considering action a*
# ▬ Compute the delta value between the previous and the new V(S)
# Output: an optimal pi* and associated V-values
class PlayerMDP:
    def __init__(self, policy=None, discountFactor=0.99, errorPrecision=0.1):
        super().__init__()
        self.discountFactor = discountFactor
        self.errorPrecision = errorPrecision
        self.policy = policy
        self.rewards = {}  # une structure qui stocke la valeur moyenne d'exécuter une action depuis un état donné.
        self.transition = {}  # etat en plus, ajouter pour chaque valeur rencontrée
        # Chercher le fichier => parsing => function de récompense et transition
        self.learn('resources/transition-log.txt')

    def BelmanValueOf(transition, reward, s, a, defaultValues, gamma=0.99):
        expectedGains = 0
        for sp in transition[s][a]:
            expectedGains += transition[s][a][sp] * defaultValues[sp]
        return reward[s][a] + gamma * expectedGains

    def actions(self, s):
        return list(self[s].keys())

    def valueIteration(self, reward, gamma=0.99, epsilon=0.01):
        pi = {s: self.actions(self, s)[0] for s in self}
        values = {s: 0.0 for s in self}
        maxDiffValue = epsilon + 1
        while maxDiffValue > epsilon:
            # for each state
            maxDiffValue = 0.0
            values = {s: 0.0 for s in self}
            for s in self:
                bestValue = self.BelmanValueOf(self, reward, s, pi[s], values, gamma)
                # search the best couple action / value
                for a in self[s]:
                    value = self.BelmanValueOf(self, reward, s, a, values)
                    if value > bestValue:
                        bestValue = value
                        pi[s] = a
                if abs(bestValue - values[s]) > maxDiffValue:
                    maxDiffValue = abs(bestValue - values[s])
                values[s] = bestValue
            values = values
        return pi, values

    def write(self, filename):
        f = open(filename, "w")
        f.write(json.dumps(self.policy, sort_keys=True, indent=2))
        f.close()

    def read(self, filename):
        f = open(filename, "r")
        self.policy = json.loads(f.read())
        f.close()

    def learn(self, filename):
        f = open(filename, "r")

        for line in f:
            t = line.split(' ')
            initState = t[0]
            action = t[1]
            reachedState = t[2]
            reward = float(t[3])
            #coucou

        f.close()


def main():
    # passer le fichier policy
    player = PlayerMDP()


# Activate default interface :


if __name__ == '__main__':
    main()
