from bin import Bin
from heuristics import BestFit, FirstFit, NextFit, WorstFit


class TabuSearch:
    heuristic_map = {
        "f": FirstFit,
        "n": NextFit,
        "w": WorstFit,
        "b": BestFit,
    }

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
        pass
