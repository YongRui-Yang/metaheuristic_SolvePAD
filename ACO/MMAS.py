import numpy as np
from board import Board
import random

class Ant:
    def __init__(self, start, bead_board_str, pheromone, alpha=1, beta=1):
        self.current_position = start
        self.start_position = start
        self.bead_board = np.array(list(bead_board_str)).reshape(5, 6)
        self.board = Board()
        self.board.initialize_board(bead_board_str)
        self.pheromone = pheromone
        self.alpha = alpha
        self.beta = beta
        self.path = []  # Initialized with an empty path
        self.score = 0
        

    def get_neighbours(self):
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, right, down, left
        neighbours = []
        for i, d in enumerate(directions):
            new_position = (self.current_position[0] + d[0], self.current_position[1] + d[1])
            if 0 <= new_position[0] < self.bead_board.shape[0] and 0 <= new_position[1] < self.bead_board.shape[1]:
                neighbours.append(i)  # Only add valid neighbours
        return neighbours

    def pick_next_move(self):
        neighbours = self.get_neighbours()
        pheromone = np.array([self.pheromone[self.current_position[0]][self.current_position[1]][i] for i in neighbours])
        scores = np.array([self.score_move(n) for n in neighbours])
        probs = pheromone ** self.alpha * scores ** self.beta
        if len(self.path)>0:
            back = (self.path[-1]+2)%4
            probs[neighbours.index(back)] = 0
        probs /= probs.sum()
        move = np.random.choice(neighbours, p=probs)  # Choose from valid neighbours
        return move

    def score_move(self, move_direction):
        # Here you would implement your scoring function
        # Firstly, update the position
        new_position = self.update_position(self.current_position, move_direction)
        # Then, append the move to the current path
        temp_path = self.path.copy()
        temp_path.append(move_direction)
        # Use the FF function to score the current move
        temp_path_str=''.join(str(x) for x in temp_path)
        board.make_move(self.start_position[0],self.start_position[1],temp_path_str)
        score = board.cpmpute_scroce()
        board.reset_board()
        # score = FF(self.bead_board, temp_path)
        return score
    
    def update_bead_board(self, move_direction):
        # Here you would implement your bead board update function
        pass

    def update_position(self, current_position, move_direction):
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, right, down, left
        return (current_position[0] + directions[move_direction][0],
                current_position[1] + directions[move_direction][1])

    def make_move(self, move_direction):
        # Score the move by your objective function
        # gained_score = self.score_move(move_direction)
        # self.score += gained_score
        path_str=''.join(str(x) for x in self.path)
        board.make_move(self.start_position[0],self.start_position[1],path_str)
        self.score = board.cpmpute_scroce()
        board.reset_board()
        # Update the bead board
        # self.update_bead_board(move_direction)
        # Add the move to the path
        self.path.append(move_direction)
        
        # Update current position based on the move_direction
        self.current_position = self.update_position(self.current_position, move_direction)

    def make_moves(self, num_moves):
        for _ in range(num_moves):
            next_move = self.pick_next_move()
            self.path.append(next_move)
            self.current_position = self.update_position(self.current_position, next_move)
            # self.make_move(next_move)
        
        path_str=''.join(str(x) for x in self.path)
        board.make_move(self.start_position[0],self.start_position[1],path_str)
        self.score = board.cpmpute_scroce()
        board.reset_board()
        

class AntColonyOptimizer:
    def __init__(self, bead_board_str, n_ants, alpha=1, beta=1, evaporation_rate=0.1):
        self.bead_board = np.array(list(bead_board_str)).reshape(5, 6)
        self.bead_board_str = bead_board_str
        self.n_ants = n_ants
        self.pheromone = np.ones((5, 6, 4))
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.ants = [Ant((random.randint(0,4), random.randint(0,5)), self.bead_board_str, self.pheromone, alpha=self.alpha, beta=self.beta) for _ in range(self.n_ants)]
        self.tau_max = 1.0  # maximum pheromone limit
        self.tau_min = 0.1  # minimum pheromone limit
        
    def make_move(self):
        for ant in self.ants:
            next_move = ant.pick_next_move()
            ant.make_move(next_move)
    
    def make_moves(self, num_moves):
        for ant in self.ants:
            ant.make_moves(num_moves)

    # def update_pheromones(self):
    #     self.pheromone *= (1 - self.evaporation_rate)  # Evaporation
    #     for ant in self.ants:
    #         for i, move in enumerate(ant.path):
    #             self.pheromone[ant.current_position[0]][ant.current_position[1]][move] += 1 / (i + 1)  # Deposit pheromone
    def update_pheromones(self):
        self.pheromone *= (1 - self.evaporation_rate)  # Evaporation
        best_ant = max(self.ants, key=lambda ant: ant.score)  # select the best ant
        for i, move in enumerate(best_ant.path):
            updated_pheromone = best_ant.score + self.pheromone[best_ant.current_position[0]][best_ant.current_position[1]][move]
            self.pheromone[best_ant.current_position[0]][best_ant.current_position[1]][move] = np.clip(updated_pheromone, self.tau_min, self.tau_max)  # apply limits

    def optimize_move(self, max_iterations=100):
        best_path = None
        best_score = -np.inf
        for it in range(max_iterations):
            self.make_move()
            self.update_pheromones()
            for ant in self.ants:
                if ant.score > best_score:
                    best_path = ant.path.copy()
                    best_score = ant.score
                    print(it,best_score)
            if it%36==0:
                self.ants = [Ant((random.randint(0,4), random.randint(0,5)), self.bead_board_str, self.pheromone, alpha=self.alpha, beta=self.beta) for _ in range(self.n_ants)]
        return best_path, best_score

    def optimize_moves(self, max_iterations=100, num_moves=30):
        best_path = None
        best_score = -np.inf
        stagnation_counter = 0
        max_stagnation = 10  # or any number based on your choice
        previous_best_score = -np.inf
        for it in range(max_iterations):
            self.make_moves(num_moves)
            self.update_pheromones()
            for ant in self.ants:
                if ant.score > best_score:
                    best_path = ant.path.copy()
                    best_score = ant.score
                    print(it,ant.start_position,best_path,len(best_path), best_score)
            # Check if the best score is not improving
            if best_score <= previous_best_score:
                stagnation_counter += 1
            else:
                stagnation_counter = 0
            previous_best_score = best_score
            # If the stagnation counter reaches a certain limit, reinitialize the pheromone values
            if stagnation_counter >= max_stagnation:
                self.pheromone.fill(self.tau_max)
                stagnation_counter = 0
            if it%12==0:
                self.ants = [Ant((random.randint(0,4), random.randint(0,5)), self.bead_board_str, self.pheromone, alpha=self.alpha, beta=self.beta) for _ in range(self.n_ants)]
        return best_path, best_score

seed_value = 11
np.random.seed(seed_value)
random.seed(seed_value)
board = Board()
board.initialize_board("DEDDEEBBEDFEBADCBAEFFAEDDFFEFB")
bead_board = board.boardstring()
ACOs = AntColonyOptimizer(bead_board,30)
best_path, best_score=ACOs.optimize_moves(500,3)
print(best_path,len(best_path), best_score)