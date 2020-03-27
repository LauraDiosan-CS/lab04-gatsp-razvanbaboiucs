import random


def generate_permutation(length, start_point=0):
    """
        Returns a permutation with starting_point on the first position
        :param length: Integer
        :param start_point: Integer (default value = 0)
        :return: Array of integers
    """
    random_list = list(range(1, length))
    random.shuffle(random_list)  # random_list has been rearranged in a random order
    random_list.insert(0, 0)
    return random_list


import tsplib95 as tsp
import numpy as np
import networkx as nx

def read_tsp_file(file_name_input):
    tsp_problem = tsp.load_problem(file_name_input)
    G = tsp_problem.get_graph()
    print(G.adj)
    n=len(G.nodes())
    network = {}
    network['number_of_nodes']=n
    matrix=nx.to_numpy_matrix(G)
    network['matrix']=matrix
    return network


file_name = "berlin52.txt"
network = read_tsp_file(file_name)
print(network['matrix'])