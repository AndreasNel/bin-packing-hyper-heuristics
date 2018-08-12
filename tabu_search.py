from bin import Bin
from heuristics import BestFit, FirstFit, NextFit, WorstFit
from move_operators import Add, Change, Remove, Swap
import random


class TabuSearch:
    MAX_COMBINATION_LENGTH = 10
    MAX_ITERATIONS = 5000
    MAX_NO_CHANGE = 100
    heuristic_map = {
        "f": FirstFit,
        "n": NextFit,
        "w": WorstFit,
        "b": BestFit,
    }
    movers = [Add, Change, Remove, Swap]

    def __init__(self, capacity, items):
        """
        Creates an instance that can run the tabu search algorithm.
        :param capacity: The capacity of a bin.
        :param items: The items that have to be packed in bins.
        """
        self.bin_capacity = capacity
        self.items = items
        self.fitness = 0
        self.bins = [Bin(capacity)]
        self.tabu_list = set()

    def run(self):
        """
        Runs the tabu search algorithm.
        """
        combination = "".join(
            [random.choice(self.heuristic_map.keys()) for _ in range(random.choice(self.MAX_COMBINATION_LENGTH) or 1)])
        self.bins = self.generate_solution(combination)
        self.fitness = sum(b.fitness() for b in self.bins) / len(self.bins)
        self.tabu_list.add(combination)
        current_iteration = 0
        num_no_change = 0
        while num_no_change >= self.MAX_NO_CHANGE or current_iteration >= self.MAX_ITERATIONS:
            combination = self.apply_move_operator(combination)
            if combination not in self.tabu_list:
                self.tabu_list.add(combination)
                solution = self.generate_solution(combination)
                fitness = sum(b.fitness() for b in solution) / len(solution)
                if fitness > self.fitness:
                    self.bins = solution
                    self.fitness = fitness
                    num_no_change = 0
            current_iteration += 1
            num_no_change += 1

    def generate_solution(self, pattern):
        """
        Generates a candidate solution based on the pattern given.
        :param pattern: A pattern indicating the order in which heuristics need to be applied to get the solution.
        :return: A list of bins to serve as a solution.
        """
        solution = [Bin(self.bin_capacity)]
        pattern_length = len(pattern)
        for idx, item in enumerate(self.items):
            h = pattern[idx % pattern_length]
            solution = self.heuristic_map[h].apply(item, solution)
        return solution

    def apply_move_operator(self, pattern):
        """
        Applies a random move operator to the given pattern.
        :param pattern: The pattern to apply the move operator to.
        :return: The pattern after the move operator has been applied.
        """
        return random.choice(self.movers).apply(pattern, self.heuristic_map.keys())[:self.MAX_COMBINATION_LENGTH]
