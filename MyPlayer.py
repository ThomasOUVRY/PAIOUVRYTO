import game421 as game


# https://ceri-num.gitbook.io/fa-paio/agir-et-apprendre-a-agir/1-intro-cpia
# Agent as a very simple UI
class MyPlayer(game.AbsAgent):

    def perceive(self, reachedStateStr, reward):
        self.state = reachedStateStr

    def decide(self, isValidAction):
        stateDico = self.stateDico()
        roll = "roll"
        keep = "keep"
        delimiter = "-"
        decisions = [roll, roll, roll]

        # D3 => Reroll sauf si 1
        # D2 => Roll sauf si 1 ou 2
        # D3 => Roll sauf 4
        if stateDico['D3'] == '1':
            decisions[2] = keep
        if stateDico['D2'] <= '2':
            decisions[1] = keep
        if stateDico['D1'] == '4':
            decisions[0] = keep
        self.action = delimiter.join(decisions)

        print("State: " + str(stateDico))
        print("Action: " + self.action)
        return self.action


rerolls = 1000
total_score = 0
player = MyPlayer()
for i in range(0, rerolls):
    gameEngine = game.System()
    gameEngine.run(player)
    total_score += player.score
    # print("Score: " + str(player.score))

print("Score moyen :" + str(total_score / rerolls))

# State: {'Horizon': '2', 'D1': '4', 'D2': '2', 'D3': '1'}
# Action: roll-roll-roll
# State: {'Horizon': '1', 'D1': '5', 'D2': '3', 'D3': '1'}
# Action: roll-roll-roll
# Score: 0
