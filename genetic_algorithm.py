from bin import Bin
from heuristics import BestFit, FirstFit, NextFit, WorstFit
import random


class GeneticAlgorithm:
    POPULATION_SIZE = 50
    MAX_GENERATIONS = 250
    MAX_NO_CHANGE = 50
    TOURNAMENT_SIZE = 20
    MUTATION_RATE = 0.3
    CROSSOVER_RATE = 0.6

    def __init__(self, capacity, items):
        """
        Creates an instance that can run the genetic algorithm.
        :param capacity: The capacity of a bin.
        :param items: The items that have to be packed in bins.
        """
        self.items = items
        self.best_solution = None
        self.population = [Chromosome(capacity) for _ in range(self.POPULATION_SIZE)]
        self.update_individuals(self.population)

    def run(self):
        """
        Runs the genetic algorithm and returns the results at the end of the process.
        :return: (num_iterations, num_no_changes)
        """
        current_iteration = 0
        num_no_change = 0
        while num_no_change < self.MAX_NO_CHANGE and current_iteration < self.MAX_GENERATIONS:
            new_generation = []
            while len(new_generation) < self.POPULATION_SIZE:
                # Select parents
                parent1 = self.select_parent()
                parent2 = self.select_parent()
                # Apply genetic operators
                child1, child2 = self.crossover(parent1, parent2)
                child1, child2 = self.mutate(child1), self.mutate(child2)
                # Update the fitness values of the offspring to determine whether they should be added
                self.update_individuals([child1, child2])
                sorted_list = sorted([parent1, parent2, child1, child2], key=lambda x: x.fitness, reverse=True)
                # Add to new generation the two best chromosomes of the combined parents and offspring
                new_generation.append(sorted_list[0])
                new_generation.append(sorted_list[1])
            self.population = new_generation
            prev_best = self.best_solution
            # Evaluate fitness values
            self.best_solution = self.update_individuals(self.population)
            # Check if any improvement has happened.
            if not prev_best or prev_best.fitness == self.best_solution.fitness:
                num_no_change += 1
            else:
                num_no_change = 0
            current_iteration += 1
        return current_iteration, num_no_change

    def mutate(self, chromosome):
        """
        Attempts to mutate the chromosome by replacing a random heuristic in the chromosome by a generated pattern.
        :param chromosome: The chromosome to mutate.
        :return: The mutated chromosome.
        """
        pattern = list(chromosome.pattern)
        if random.random() < self.MUTATION_RATE:
            mutation_point = random.randrange(len(pattern))
            pattern[mutation_point] = Chromosome.generate_pattern()
        return Chromosome(chromosome.bin_capacity, "".join(pattern))

    def crossover(self, parent1, parent2):
        """
        Attempt to perform crossover between two chromosomes.
        :param parent1: The first parent.
        :param parent2: The second parent.
        :return: The two individuals after crossover has been performed.
        """
        pattern1, pattern2 = parent1.pattern, parent2.pattern
        if random.random() < self.CROSSOVER_RATE:
            point1, point2 = random.randrange(len(pattern1)), random.randrange(len(pattern2))
            substr1, substr2 = pattern1[point1:], pattern2[point2:]
            pattern1, pattern2 = "".join((pattern1[:point1], substr2)), "".join((pattern2[:point2], substr1))
        return Chromosome(parent1.bin_capacity, pattern1), Chromosome(parent2.bin_capacity, pattern2)

    def update_individuals(self, individuals):
        """
        Update the fitness values of all the chromosomes in the population.
        """
        for individual in individuals:
            solution = individual.generate_solution(self.items)
            individual.num_bins = len(solution)
            individual.fitness = sum(b.fitness() for b in solution) / len(solution)
        return max(self.population, key=lambda x: x.fitness)

    def select_parent(self):
        """
        Selects a parent from the current population by applying tournament selection.
        :return: The selected parent.
        """
        candidate = random.choice(self.population)
        for _ in range(self.TOURNAMENT_SIZE - 1):
            opponent = random.choice(self.population)
            if opponent.fitness > candidate.fitness:
                candidate = opponent
        return candidate


class Chromosome:
    MAX_COMBINATION_LENGTH = 10
    heuristic_map = {
        "f": FirstFit,
        "n": NextFit,
        "w": WorstFit,
        "b": BestFit,
    }

    def __init__(self, capacity, pattern=None):
        self.bin_capacity = capacity
        self.fitness = 0
        self.num_bins = 0
        self.pattern = pattern or self.generate_pattern()

    @staticmethod
    def generate_pattern():
        """
        Generates a random pattern.
        :return: The generated pattern string.
        """
        return "".join(
            [random.choice(list(Chromosome.heuristic_map.keys())) for _ in range(random.randrange(Chromosome.MAX_COMBINATION_LENGTH) or 1)])

    def generate_solution(self, items):
        """
        Generates a candidate solution based on the pattern given.
        :param items: The items that need to be used when generating a solution.
        :return: A list of bins to serve as a solution.
        """
        solution = [Bin(self.bin_capacity)]
        pattern_length = len(self.pattern)
        for idx, item in enumerate(items):
            h = self.pattern[idx % pattern_length]
            solution = self.heuristic_map[h].apply(item, solution)
        return solution
