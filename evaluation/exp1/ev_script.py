import time

import pm4py
from pm4py.algo.simulation.tree_generator.algorithm import apply as tree_gen
from pm4py.objects.powl.obj import POWL

import os
import csv

from utils.pn_to_powl.converter import convert_workflow_net_to_powl


def get_leaves(model: POWL):
    if model.children:
        res = []
        for child in model.children:
            res = res + get_leaves(child)
        return res
    else:
        if model.label:
            return [model]
        else:
            return []


base_directory = r"C:\Users\kourani\git\ProMoAI\utils\pn_to_powl\evaluation\exp1"

trees_directory = os.path.join(base_directory, "process_trees")
os.makedirs(trees_directory, exist_ok=True)

csv_file = os.path.join(base_directory, "statistics.csv")

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Iteration", "Time (sec)", "Transitions", "Labeled Transitions", "Places", "Arcs", "POWL Leaves"])

for i in range(1, 1001):

    tree = tree_gen(parameters={"min": 10, "mode": 50, "max": 200})
    tree_file = os.path.join(trees_directory, f"tree_{i}.ptml")
    pm4py.write_ptml(tree, tree_file)
    pn, im, fm = pm4py.convert_to_petri_net(tree)
    start_time = time.time()
    try:
        powl_model = convert_workflow_net_to_powl(pn)
    except:
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i, "error"])
    else:
        end_time = time.time()
        time_taken = end_time - start_time
        num_transitions = len(pn.transitions)
        labeled_transitions = len([t for t in pn.transitions if t.label])
        num_places = len(pn.places)
        num_arcs = len(pn.arcs)
        num_leaves = len(get_leaves(powl_model))

        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i, time_taken, num_transitions, labeled_transitions, num_places, num_arcs, num_leaves])
