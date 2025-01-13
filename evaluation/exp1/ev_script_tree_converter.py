import time
import pm4py
import os
import csv


base_directory = r"C:\Users\kourani\PycharmProjects\WF-to-POWL\evaluation\exp1"

tree_directory = os.path.join(base_directory, "process_trees")

csv_file = os.path.join(base_directory, "time_tree_converter.csv")

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["ID", "Tree Time (sec)"])

for i in range(1, 1001):
    tree_path = os.path.join(tree_directory, f"tree_{i}.ptml")
    tree = pm4py.read_ptml(tree_path)

    pn, im, fm = pm4py.convert_to_petri_net(tree)
    stats = [f"{i}"]

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
        print(stats)
        writer.writerow(stats)
