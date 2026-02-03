import os
import time
import pandas as pd
import pm4py
import powl

from implementation_old.converter import convert_workflow_net_to_powl as old_converter
from powl.conversion.to_powl.from_pn.converter import convert_workflow_net_to_powl as new_converter
from pm4py import convert_to_process_tree as tree_converter

data_set = "SAP RM"
base_directory = r"C:\Users\kourani\PycharmProjects\WF-to-POWL\evaluation\exp2_updated"

PATH_TO_MODELS = os.path.join(base_directory, data_set)
TREE_PATH = os.path.join(base_directory, "generated trees")
POWL_PATH = os.path.join(base_directory, "generated POWL OLD")
POWL_20_PATH = os.path.join(base_directory, "generated POWL 20")

os.makedirs(TREE_PATH, exist_ok=True)
os.makedirs(POWL_PATH, exist_ok=True)
os.makedirs(POWL_20_PATH, exist_ok=True)


csv_file = os.path.join(base_directory, f"{data_set} results.csv")

summary_csv_file = os.path.join(base_directory, f"{data_set} summary.csv")

results = []

files = [f for f in os.listdir(PATH_TO_MODELS) if f.endswith('.pnml')]
print(f"Found {len(files)} models. Starting benchmark...")

stats = {
    "tree": {"total": 0, "success": 0, "failure": 0},
    "old_powl": {"total": 0, "success": 0, "failure": 0},
    "powl2": {"total": 0, "success": 0, "failure": 0},
}

for filename in files:
    print(f"Processing {filename}")

    file_path = os.path.join(PATH_TO_MODELS, filename)
    row = {
        "filename": filename,
        "transitions": 0,
        "places": 0,
        "size_sum": 0,
        "tree_time": "n/a",
        "old_powl_time": "n/a",
        "powl2_time": "n/a"
    }

    net, im, fm = pm4py.read_pnml(file_path)

    t_count = len(net.transitions)
    p_count = len(net.places)
    row["transitions"] = t_count
    row["places"] = p_count
    row["size_sum"] = t_count + p_count


    try:
        start = time.time()
        tree = tree_converter(net, im, fm)
        end = time.time()
        row["tree_time"] = end - start
        stats["tree"]["success"] += 1
        pm4py.save_vis_process_tree(tree, os.path.join(TREE_PATH, f"{filename}.svg"))
    except Exception as e:
        row["tree_time"] = f"Error: {str(e)}"
        stats["tree"]["failure"] += 1

    try:
        start = time.time()
        old_powl = old_converter(net)
        end = time.time()
        row["old_powl_time"] = end - start
        stats["old_powl"]["success"] += 1
        pm4py.save_vis_powl(old_powl, os.path.join(POWL_PATH, f"{filename}.svg"))
    except Exception as e:
        row["old_powl_time"] = f"Error: {str(e)}"
        stats["old_powl"]["failure"] += 1

    try:
        start = time.time()
        new_powl = new_converter(net)
        end = time.time()
        row["powl2_time"] = end - start
        stats["powl2"]["success"] += 1
        powl.save_visualization(new_powl, os.path.join(POWL_20_PATH, f"{filename}.svg"))
    except Exception as e:
        row["powl2_time"] = f"Error: {str(e)}"
        stats["powl2"]["failure"] += 1

    results.append(row)
    print(f"Processed {filename} | Size: {row['size_sum']} | P2: {row['powl2_time']}s")

df = pd.DataFrame(results)
df.to_csv(csv_file, index=False)
print(f"\nBenchmark complete. Results saved to {csv_file}")

summary_rows = []

for key, values in stats.items():
    summary_rows.append({
        "converter": key,
        "total_cases": values["success"] + values["failure"],
        "successes": values["success"],
        "failures": values["failure"]
    })

summary_df = pd.DataFrame(summary_rows)
summary_df.to_csv(summary_csv_file, index=False)

print("\nSummary Report:")
print(summary_df)
print(f"\nSummary saved to {summary_csv_file}")