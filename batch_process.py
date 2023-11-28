import argparse
from plot import plot
from speedup import speedup
import os
import total_plot


def process_folders(directory):

    all_files = []

    for root, dirs, files in os.walk(directory):

        for file in files:
            if file.endswith("_speedup.json"):
                continue
            if file.endswith(".json"):
                filepath = os.path.join(root, file)
                all_files.append(filepath.split(".json")[0] + "_speedup.json")
                speedup(filepath)
                plot(filepath)

    print(all_files)
    total_plot.plot_total(all_files)


if __name__ == "__main__":
    # Call the function with the desired directory

    parser = argparse.ArgumentParser(
        description="Generate physical operator labels for input queries and save to json")

    parser.add_argument("context", default=None,
                        help="File in which queries results are located")
    args = parser.parse_args()
    process_folders(args.context)
