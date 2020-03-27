from random import randint
from Utils import generate_permutation


class Chromosome:
    def __init__(self, parameters=None):
        self.__parameters = parameters
        self.__representation = generate_permutation(self.__parameters['number_of_nodes'])
        self.__fitness = 0.0

    @property
    def representation(self):
        return self.__representation

    @property
    def fitness(self):
        return self.__fitness

    @representation.setter
    def representation(self, new_representation=[]):
        self.__representation = new_representation

    @fitness.setter
    def fitness(self, new_fitness=0.0):
        self.__fitness = new_fitness

    def crossover(self, chromosome):
        """
            Order_1 crossover
            :param chromosome: Chromosome
            :return: Chromosome
        """
        position_1 = randint(1, self.__parameters['number_of_nodes'] - 1)
        position_2 = randint(1, self.__parameters['number_of_nodes'] - 1)
        if position_1 > position_2:
            position_1, position_2 = position_2, position_1
        new_representation = self.__representation[position_1: position_2]
        new_representation.insert(0, 0)
        position_to_add = 1
        for element in chromosome.representation[position_2 : ] + chromosome.representation[ : position_2]:
            if element not in new_representation:
                if len(new_representation) < self.__parameters['number_of_nodes'] - position_1:
                    new_representation.append(element)
                else:
                    new_representation.insert(position_to_add, element)
                    position_to_add += 1
        offspring = Chromosome(self.__parameters)
        offspring.representation = new_representation
        return offspring

    def mutation(self):
        position_1 = randint(1, self.__parameters['number_of_nodes'] - 1)
        position_2 = randint(1, self.__parameters['number_of_nodes'] - 1)
        if position_2 < position_1:
            position_1, position_2 = position_2, position_1
        el = self.__representation[position_2]
        del self.__representation[position_2]
        self.__representation.insert(position_1 + 1, el)

    def __str__(self):
        return 'Chromosome: ' + str(self.__representation) + ' has fitness: ' + str(self.__fitness)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, c):
        return self.__representation == c.__representation and self.__fitness == c.__fitness
