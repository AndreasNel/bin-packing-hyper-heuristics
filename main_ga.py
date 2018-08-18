from genetic_algorithm import GeneticAlgorithm
from item import Item
from random import shuffle
from datetime import datetime
import json


def log(message, end=None):
    print(message, flush=True, end=end)


if __name__ == '__main__':
    datasets = [
        {"name": "N1C1W1_A.BPP", "results": {}},
        {"name": "N2C2W1_B.BPP", "results": {}},
        {"name": "N3C3W1_C.BPP", "results": {}},
        {"name": "N4C1W1_D.BPP", "results": {}},
        {"name": "N4C3W1_E.BPP", "results": {}},
        {"name": "N1W1B1R0.BPP", "results": {}},
        {"name": "N2W1B1R1.BPP", "results": {}},
        {"name": "N3W1B1R2.BPP", "results": {}},
        {"name": "N4W1B1R3.BPP", "results": {}},
        {"name": "N4W4B3R4.BPP", "results": {}},
        {"name": "HARD1.BPP", "results": {}},
        {"name": "HARD2.BPP", "results": {}},
        {"name": "HARD3.BPP", "results": {}},
        {"name": "HARD4.BPP", "results": {}},
        {"name": "HARD5.BPP", "results": {}},
    ]

    # Loop through each data set.
    for dataset in datasets:
        # Read the data into memory
        with open('datasets/{}'.format(dataset["name"]), 'r') as file:
            data = file.read().splitlines()
            num_items, capacity, items = int(data[0]), int(data[1]), data[2:]
            log("\n\nDATASET {}: num_items {} capacity {} items_read {}".format(dataset["name"], num_items, capacity, len(items)))
        items = [Item(size=int(i)) for i in items]
        log("  Iteration", end=" ")
        # Perform 30 independent iterations.
        for iteration in range(30):
            log(iteration+1, end=" ")
            # Randomize the order of the items in the item list.
            shuffle(items)
            thing = GeneticAlgorithm(capacity, items)

            start_time = datetime.now()
            total_iterations, stagnation = thing.run()
            execution_time = datetime.now() - start_time

            # Record the relevant data for analysis
            summary = {
                "execution_time": str(execution_time),
                "num_bins": thing.best_solution.num_bins,
                "fitness": thing.best_solution.fitness,
                "iterations": total_iterations,
                "stagnation": stagnation,
                "combination": thing.best_solution.pattern,
            }
            dataset["results"].setdefault("GA", []).append(summary)
    # Write the captured data to disk.
    with open("results_ga.json", "w") as file:
        file.write(json.dumps(datasets, indent=2))
