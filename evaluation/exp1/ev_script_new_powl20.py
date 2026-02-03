import time
import pm4py
import os
import csv

from powl.conversion.to_powl.from_pn.converter import convert_workflow_net_to_powl as new_converter
from powl.objects.obj import POWL
import powl

base_directory = r"C:\Users\kourani\PycharmProjects\WF-to-POWL\evaluation\exp1"

tree_directory = os.path.join(base_directory, "process_trees")

csv_file = os.path.join(base_directory, "statistics_powl20.csv")

POWL_20_PATH = os.path.join(base_directory, "generated POWL 20")

os.makedirs(POWL_20_PATH, exist_ok=True)


def get_leaves(model: POWL):
    if model.children:
        leaves = []
        for child in model.children:
            leaves = leaves + get_leaves(child)
        return leaves
    else:
        if model.label:
            return [model]
        else:
            return []

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Iteration", "Time Total (sec)", "Transitions", "Labeled Transitions", "Places", "Arcs", "POWL Leaves"])

for i in range(1, 1001):
    print("Iteration", i)
    tree_path = os.path.join(tree_directory, f"tree_{i}.ptml")
    tree = pm4py.read_ptml(tree_path)

    pn, im, fm = pm4py.convert_to_petri_net(tree)

    start_time = time.time()
    powl_model = new_converter(pn)
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
