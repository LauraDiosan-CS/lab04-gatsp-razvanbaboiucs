# %% md

# TSP
## Traveling Salesman Problem

# %% md


# %% md

#### Implementation of GA class :

# %%
import networkx as nx

from Chromosome import Chromosome
from random import randint as rnd


class GeneticAlgorithm:

    def __init__(self, ga_parameters_input, chromosome_parameters_input):
        """
            ga_parameters keys : population_size, evaluation_function
            chromosome_parameters keys : number_of_nodes
            :param ga_parameters_input: Dictionary
            :param chromosome_parameters_input: Dictionary
        """
        self.__chromosome_parameters = chromosome_parameters_input
        self.__ga_parameters = ga_parameters_input
        self.__population = []

    @property
    def population(self):
        return self.__population

    def initialisation(self):
        """
            Initializes the population for the first generation
        """
        for _ in range(self.__ga_parameters['population_size']):
            c = Chromosome(self.__chromosome_parameters)
            self.__population.append(c)

    def evaluation(self):
        """
            Evaluates every chromosome in the current population
                (sets the fitness)
        """
        for chromosome in self.__population:
            chromosome.fitness = self.__ga_parameters['evaluation_function'](chromosome.representation)

    def evaluate_one(self, chromosome):
        """
            Evaluates the given chromosome (sets the fitness)
            :param chromosome: Chromosome
        """
        chromosome.fitness = self.__ga_parameters['evaluation_function'](chromosome.representation)

    def best_chromosome(self):
        """
            Returns the best chromosome in the current population
            :return: Chromosome
        """
        best = self.__population[0]
        for chromosome in self.__population:
            if chromosome.fitness < best.fitness:
                best = chromosome
        return best

    def worst_chromosome(self):
        """
            Returns the worst chromosome in the current population
            :return: Chromosome
        """
        worst = self.__population[0]
        for chromosome in self.__population:
            if chromosome.fitness > worst.fitness:
                worst = chromosome
        return worst

    def selection(self):
        """
            Returns a chromosome from the current population
            :return: Chromosome
        """
        # TODO: better selection
        position_1 = random.randint(0, self.__ga_parameters['population_size'] - 1)
        position_2 = random.randint(0, self.__ga_parameters['population_size'] - 1)
        if self.__population[position_1].fitness < self.__population[position_2].fitness:
            return self.__population[position_1]
        else:
            return self.__population[position_2]

    def next_generation(self):
        """
            Creates the next generation by crossing over chromosomes
                from the current population and mutating them
        """
        next_population = [self.best_chromosome()]
        for _ in range(self.__ga_parameters['population_size'] - 1):
            # TODO: better selection (no two identical chromosomes)
            chromosome_1 = self.selection()
            chromosome_2 = self.selection()
            offspring = chromosome_1.crossover(chromosome_2)
            offspring.mutation()
            self.evaluate_one(offspring)
            worst_chromosome = self.worst_chromosome()
            if offspring.fitness > worst_chromosome.fitness:
                offspring = worst_chromosome
            next_population.append(offspring)
        self.__population = next_population


# %% md

#### Fitness calculation function:

# %%

def get_fitness(representation):
    """
        Gets a certain representation from a chromosome and returns its
            fitness by calculating the sum of the edges
        :param representation: Array of integers
        :return: Integer
    """
    fitness = 0
    matrix = network['matrix']
    for k in range(len(representation) - 1):
        node_1 = representation[k]
        node_2 = representation[k + 1]
        fitness += matrix[node_1][node_2]
    # adding the distance from the last node back to the first one to close the circuit
    node_1 = representation[len(representation) - 1]  # last node
    node_2 = representation[0]  # first node
    fitness += matrix[node_1][node_2]
    return fitness


# %% md

#### Read network function:

# %%

def read_network(file_name_input):
    """
        Reads the network found in file_name
        :param file_name_input: String
        :return: Dictionary
    """
    file = open(file_name_input, "r")
    network_dictionary = {}
    number_of_nodes = int(file.readline())
    network_dictionary['number_of_nodes'] = number_of_nodes
    matrix = []
    for i in range(number_of_nodes):
        line = file.readline()
        line_array = line.split(',')
        matrix.append([])
        for j in range(len(line_array)):
            value = int(line_array[j])
            matrix[i].append(value)
    network_dictionary['matrix'] = matrix

    return network_dictionary


import tsplib95 as tsp


def read_tsp_file(file_name_input):
    tsp_problem = tsp.load_problem(file_name_input)
    G = tsp_problem.get_graph()
    n = len(G.nodes())
    network = {}
    network['number_of_nodes'] = n
    matrix = nx.to_numpy_matrix(G)
    network['matrix'] = matrix
    return network


# %% md

#### The initializations of the variables

# %%

import random

random.seed()

file_name = "berlin52.txt"
network = read_tsp_file(file_name)
ga_parameters = {'population_size': 200, 'number_of_generations': 200, 'evaluation_function': get_fitness}
chromosome_parameters = {'number_of_nodes': network['number_of_nodes']}

# %% md

#### The graph:

# %%

# %% md

### Application of the GA:

# %%

best_solution_representation = []
best_solution_fitness = 999999

GA = GeneticAlgorithm(ga_parameters, chromosome_parameters)
GA.initialisation()
GA.evaluation()

for generation_number in range(ga_parameters['number_of_generations']):
    best_chromosome_representation = GA.best_chromosome().representation
    best_chromosome_fitness = GA.best_chromosome().fitness
    if best_chromosome_fitness < best_solution_fitness:
        best_solution_fitness = best_chromosome_fitness
        best_solution_representation = best_chromosome_representation
    print('Generation : ' + str(generation_number) + ' -- representation : ' + str(
        best_chromosome_representation) + ' -- fitness : ' + str(best_chromosome_fitness))
    GA.next_generation()
    GA.evaluation()
print("\n ----------- Solution -------------\n")
print('Solution representation : ' + str(best_solution_representation) + ' -- fitness : ' + str(best_solution_fitness))

# %% md

#### Solution graph

# %%
