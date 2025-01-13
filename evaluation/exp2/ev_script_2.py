import time

import pm4py
from pm4py.objects.powl.obj import POWL

import os
import csv

from implementation.converter import convert_workflow_net_to_powl


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


base_directory = r"C:\Users\kourani\PycharmProjects\WF-to-POWL\evaluation\exp2"

pn_directory = os.path.join(base_directory, "ground_truth_pn")
os.makedirs(pn_directory, exist_ok=True)

csv_file = os.path.join(base_directory, "statistics.csv")

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["ID", "Transitions", "Labeled Transitions", "Places", "Arcs", "POWL Time (sec)", "POWL Leaves",
                     "Tree Time (sec)"])

for i in range(1, 21):
    pn_path = os.path.join(pn_directory, f"{i:02}.pnml")
    pn, im, fm = pm4py.read_pnml(pn_path)
    num_transitions = len(pn.transitions)
    labeled_transitions = len([t for t in pn.transitions if t.label])
    num_places = len(pn.places)
    num_arcs = len(pn.arcs)
    stats = [f"{i:02}", num_transitions, labeled_transitions, num_places, num_arcs]

    # convert to POWL
    start_time = time.time()
    try:
        powl_model = convert_workflow_net_to_powl(pn)
    except:
        stats = stats + ["error", "error"]
    else:
        end_time = time.time()
        time_taken = end_time - start_time
        num_leaves = len(get_leaves(powl_model))
        stats = stats + [time_taken, num_leaves]

    # convert to tree
    start_time = time.time()
    try:
        tree = pm4py.convert_to_process_tree(pn, im, fm)
    except:
        stats = stats + ["error"]
    else:
        end_time = time.time()
        time_taken = end_time - start_time
        stats.append(time_taken)

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(stats)
