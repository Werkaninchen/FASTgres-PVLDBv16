# data from https://allisonhorst.github.io/palmerpenguins/

import matplotlib.pyplot as plt
import numpy as np
import json
import os


def plot_total(files):

    JOB_metrics = {
        'speedupAbs': (),
        'speedupAvg': (),
        'runtime': (),
        "factor": (),
    }

    TPCH_metrics = {
        'speedupAbs': (),
        'speedupAvg': (),
        'runtime': (),
        "factor": (),
    }

    for file in files:
        if not file.endswith("_speedup.json"):
            continue

        with open(file, "r") as f:
            data = json.load(f)["avrgTOT"]
        if "JOB" in file:
            JOB_metrics['speedupAbs'] += (data["speedupAbs"],)
            JOB_metrics['speedupAvg'] += (data["speedupAvg"],)
            JOB_metrics['runtime'] += (data["runtime"],)
            JOB_metrics['factor'] += (data["factor"]*100,)
        elif "TPCH" in file:
            TPCH_metrics['speedupAbs'] += (data["speedupAbs"],)
            TPCH_metrics['speedupAvg'] += (data["speedupAvg"],)
            TPCH_metrics['runtime'] += (data["runtime"],)
            TPCH_metrics['factor'] += (data["factor"]*100,)

    thresholds = ("1.5x", "2x", "2.5x", "3x", "3.5x")

    x = np.arange(len(thresholds))  # the label locations
    width = 1/len(JOB_metrics) - .03  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in JOB_metrics.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=4)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Time (s)')
    ax.set_title('Overview')
    ax.set_xticks(x + width, thresholds)
    ax.legend(loc='upper left', ncols=4)
    # ax.set_ylim(0, 250)
    ax.set_yscale('log')
    plt.savefig("JOB_total.png")
    plt.show()


if __name__ == "__main__":
    plot_total(
        ["/Users/jeroen/FASTgres-PVLDBv16/output/new/threshold1.5/JOB_old_speedup.json", "/Users/jeroen/FASTgres-PVLDBv16/output/new/threshold1.5/JOB_old.json"])
