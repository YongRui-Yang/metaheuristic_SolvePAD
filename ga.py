import random
from board import Board
board = Board()

# 定義問題的目標函數
def fitness_function(solution):
    # 在此處計算解的適應度（目標函數的值）
    path = ''.join(str(x) for x in solution)
    board.reset_board()
    board.make_move(0,0,path)
    fitness = board.cpmpute_scroce()
    return fitness

# 初始化個體
def initialize_individual():
    # 在此處產生一個隨機的個體（解）
    individual = []
    for _ in range(10):
        gene = random.randint(0, 3)  # 隨機生成0或1
        individual.append(gene)
    return individual

# 初始化種群
def initialize_population(population_size):
    population = []
    for _ in range(population_size):
        individual = initialize_individual()
        population.append(individual)
    return population

# 計算種群中每個個體的適應度
def calculate_fitness(population):
    fitness_values = []
    for individual in population:
        fitness = fitness_function(individual)
        fitness_values.append(fitness)
    return fitness_values

# 選擇適應度較高的個體
def selection(population, fitness_values):
    # 在此處根據適應度值選擇個體進行繁殖
    # 計算適應度總和
    total_fitness = sum(fitness_values)
    
    # 計算每個個體的選擇概率
    probabilities = [fitness / total_fitness for fitness in fitness_values]
    
    # 使用輪盤選擇法選擇下一代個體
    selected_population = []
    for _ in range(len(population)):
        selected_individual = roulette_wheel_selection(population, probabilities)
        selected_population.append(selected_individual)
    
    return selected_population
def roulette_wheel_selection(population, probabilities):
    # 使用輪盤選擇法選擇個體
    cumulative_probabilities = [sum(probabilities[:i+1]) for i in range(len(probabilities))]
    random_number = random.random()
    
    for i, cumulative_probability in enumerate(cumulative_probabilities):
        if random_number <= cumulative_probability:
            return population[i]
# 交配 (交叉)
def crossover(parent1, parent2):
    # 在此處實現交配操作，產生新的後代
    # 隨機選擇交配點
    crossover_pointrate = random.random()
    
    crossover_point1 = round((len(parent1)-1)*crossover_pointrate+1)
    crossover_point2 = round((len(parent2)-1)*crossover_pointrate+1)
    # if len(parent1)>2:
    #     crossover_point1 = random.randint(1, len(parent1) - 1)
    # else:
    #     crossover_point1 = round((len(parent1)-1)*crossover_pointrate+1)
    # if len(parent2)>2:
    #     crossover_point2 = random.randint(1, len(parent2) - 1)
    # else:
    #     crossover_point2 = round((len(parent2)-1)*crossover_pointrate+1)
    # 生成兩個後代
    offspring1 = parent1[:crossover_point1] + parent2[crossover_point2:]
    offspring2 = parent2[:crossover_point2] + parent1[crossover_point1:]
    
    return offspring1, offspring2

# 突變
def mutate(individual):
    # 在此處實現突變操作，對個體進行基因突變
    mutated_individual = []
    mnum = 1    # 個體基因中突變的數量期望值
    mutation_rate = mnum/len(individual)
    for gene in individual:
        if random.random() < mutation_rate:
            # 突變操作：將基因突變（0變為1,2,3）
            mutated_gene = (gene + random.randint(1, 3))%4
        else:
            mutated_gene = gene
        mutated_individual.append(mutated_gene)
    
    mutation_add_rate = 0.1
    mutation_add_num = random.randint(1, 10)

    if random.random() < mutation_add_rate:
        for i in range(mutation_add_num):
            mutated_individual.append(random.randint(0, 3))
            
    if random.random() < mutation_add_rate:
        if(len(mutated_individual)>mutation_add_num):
            mutated_individual=mutated_individual[:-mutation_add_num]
        
            
    return mutated_individual

# 遺傳算法主循環
def genetic_algorithm(population_size, generations):
    population = initialize_population(population_size)
    best_solution = population[0]
    for _ in range(generations):
        fitness_values = calculate_fitness(population)
        
        # 選擇下一代個體
        selected_population = selection(population, fitness_values)
        
        # 進行交配操作
        offspring_population = []
        for i in range(0, len(selected_population), 2):
            parent1 = selected_population[i]
            parent2 = selected_population[i+1]
            offspring1, offspring2 = crossover(parent1, parent2)
            offspring_population.append(offspring1)
            offspring_population.append(offspring2)
        
        # 進行突變操作
        mutated_population = [mutate(individual) for individual in offspring_population]
        
        # 更新種群
        population = mutated_population
        
        # 更新最佳解
        tmp_best_solution = max(population, key=fitness_function)
        if fitness_function(best_solution) < fitness_function(tmp_best_solution):
            best_solution = tmp_best_solution
            print("Best solution:", best_solution,len(best_solution))
        
    # # 返回最佳解
    # best_solution = max(population, key=fitness_function)
    return best_solution

seed_value = 11
random.seed(seed_value)
board.initialize_board("DEDDEEBBEDFEBADCBAEFFAEDDFFEFB")


# 使用遺傳算法求解問題
best_solution = genetic_algorithm(population_size=100, generations=1000)

path = ''.join(str(x) for x in best_solution)
# 輸出最佳解
print("Best solution:", best_solution,fitness_function(path))
board.reset_board()
board.make_move(0,0,path)
x=board.cpmpute_scroce()
print(x)
board.display_board()