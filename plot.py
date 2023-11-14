import argparse
import matplotlib.pyplot as plt
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate physical operator labels for input queries and save to json")

    parser.add_argument("context", default=None,
                        help="File in which queries results are located")
    args = parser.parse_args()
    # Load the JSON data
    with open(args.context, "r") as f:
        data = json.load(f)

    # Sort the data by Query
    sorted_data = sorted(data.items(), key=lambda x: x[0])
    # Extract the speedup values
    speedup_values = []
    for key, value in sorted_data:
        if ".sql" not in key:
            continue

        speedup_values.append(value["speedup"])

    # Extract the absolute speedup values
    speedup_abs_values = []
    for key, value in sorted_data:
        if ".sql" not in key:
            continue
        speedup_abs_values.append(value["speedupAbs"])

    # Extract the Query
    opt_levels = []
    for key, _ in sorted_data:
        if ".sql" not in key:
            continue
        opt_levels.append(key.split(".sql")[0])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Speedup plot
    ax1.plot(opt_levels, speedup_values, marker='o', linestyle='-', color='b')
    ax1.set_xlabel("Query")
    ax1.set_ylabel("Speedup")
    ax1.set_title("Speedup vs. Query")
    ax1.grid(True)

    # # Absolute speedup plot
    ax2.plot(opt_levels, speedup_abs_values,
             marker='o', linestyle='-', color='b')
    ax2.set_xlabel("Query")
    ax2.set_ylabel("Absolute Speedup")
    ax2.set_title("Absolute Speedup vs. Query")
    ax2.grid(True)

    # Show the plots
    plt.tight_layout()
    plt.show()
