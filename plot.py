import argparse
import matplotlib.pyplot as plt
import json

import re


def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]


def plot(context: str):

    with open(context.split(".json")[0] + "_speedup.json", "r") as f:
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

    # opt_levels.sort(key=natural_sort_key)
    labelsize = 8
    color = '#3c3c3b'
    background_color = '#ececec'

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(48, 12))

    ax1.set_facecolor(background_color)
    ax2.set_facecolor(background_color)
    ax3.set_facecolor(background_color)
    ax4.set_facecolor(background_color)

    # Speedup plot
    ax1.bar(opt_levels, speedup_values, color=color, alpha=0.7)
    ax1.set_xlabel("Query")
    ax1.set_ylabel("Relative speedup (s)")
    ax1.set_title("Speedup vs. Query")
    ax1.xaxis.set_tick_params(rotation=90, labelsize=labelsize)
    ax1.grid(True)

    # # Absolute speedup plot

    ax2.bar(opt_levels, speedup_abs_values, color=color, alpha=0.7)
    ax2.xaxis.set_tick_params(rotation=90, labelsize=labelsize)
    ax2.set_ylabel("Absolute speedup (s)")
    ax2.set_title("Absolute Speedup vs. Query")
    ax2.grid(True)

    # Speedup plot
    ax3.bar(opt_levels, speedup_values, color=color, alpha=0.7)
    ax3.set_xlabel("Query")
    ax3.set_ylabel("Relative speedup (s)")
    ax3.set_title("Speedup vs. Query (log)")
    ax3.set_yscale('log')
    ax3.xaxis.set_tick_params(rotation=90, labelsize=labelsize)
    ax3.grid(True)

    # # Absolute speedup plot

    ax4.bar(opt_levels, speedup_abs_values, color=color, alpha=0.7)
    ax4.set_ylabel("Absolute speedup (s)")
    ax4.xaxis.set_tick_params(rotation=90, labelsize=labelsize)
    ax4.set_title("Absolute Speedup vs. Query (log)")
    ax4.set_yscale('log')
    ax4.grid(True)

    # Show the plots
    plt.tight_layout()
    plt.savefig(context+".png")
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate physical operator labels for input queries and save to json")

    parser.add_argument("context", default=None,
                        help="File in which queries results are located")
    args = parser.parse_args()
    plot(args.context)
