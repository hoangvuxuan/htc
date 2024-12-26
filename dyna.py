import random

# Game Caro 3x3
class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]  # 3x3 board (nested list)
        self.current_player = 'X'  # Player X starts

    def print_board(self):
        for row in self.board:
            print('|'.join(row))
            print("-" * 5)

    def available_actions(self):
        actions = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    actions.append((i, j))
        return actions

    def take_action(self, action):
        i, j = action
        if self.board[i][j] == ' ':
            self.board[i][j] = self.current_player
            return True
        return False

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def is_winner(self, player):
        # Check rows, columns, and diagonals
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                return True
            if all(self.board[j][i] == player for j in range(3)):
                return True

        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2 - i] == player for i in range(3)):
            return True

        return False

    def is_full(self):
        return all(self.board[i][j] != ' ' for i in range(3) for j in range(3))

    def reset(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

# Dyna-Q Algorithm for Tic-Tac-Toe
class DynaQAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1, planning_steps=5):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.planning_steps = planning_steps
        self.q_table = {}  # Q-values: key = (state, action), value = Q-value
        self.model = {}  # Model: key = (state, action), value = (next_state, reward)

    def get_q_value(self, state, action):
        return self.q_table.get((tuple(tuple(row) for row in state), action), 0.0)

    def update_q_value(self, state, action, reward, next_state):
        max_next_q = max([self.get_q_value(next_state, a) for a in self.available_actions(next_state)], default=0)
        q_value = self.get_q_value(state, action)
        new_q_value = q_value + self.learning_rate * (reward + self.discount_factor * max_next_q - q_value)
        self.q_table[(tuple(tuple(row) for row in state), action)] = new_q_value

    def plan(self):
        for _ in range(self.planning_steps):
            state, action = random.choice(list(self.model.keys()))
            next_state, reward = self.model[(state, action)]
            self.update_q_value(state, action, reward, next_state)

    def select_action(self, state, available_actions):
        if random.random() < self.exploration_rate:
            return random.choice(available_actions)
        q_values = [self.get_q_value(state, action) for action in available_actions]
        max_q_value = max(q_values)
        best_actions = [action for action, q in zip(available_actions, q_values) if q == max_q_value]
        return random.choice(best_actions)

    def learn_from_experience(self, state, action, reward, next_state):
        self.update_q_value(state, action, reward, next_state)
        self.model[(tuple(tuple(row) for row in state), action)] = (next_state, reward)

    def available_actions(self, state):
        actions = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == ' ':
                    actions.append((i, j))
        return actions

# Main loop for training the agent
def train_dyna_q():
    game = TicTacToe()
    agent = DynaQAgent()

    episodes = 5000
    for _ in range(episodes):
        game.reset()
        state = game.board
        done = False
        while not done:
            available_actions = game.available_actions()
            action = agent.select_action(state, available_actions)
            game.take_action(action)

            if game.is_winner('X'):
                reward = 10  # X wins
                done = True
            elif game.is_winner('O'):
                reward = -10  # O wins
                done = True
            elif game.is_full():
                reward = 0  # Draw
                done = True
            else:
                reward = 0  # No winner yet

            next_state = game.board
            agent.learn_from_experience(state, action, reward, next_state)
            agent.plan()  # Perform planning

            if not done:
                game.switch_player()
                state = next_state

    return agent

