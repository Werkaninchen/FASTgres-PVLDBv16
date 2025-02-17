import json
import argparse
from hint_set import HintSet


def getBase(db: str) -> dict:
    with open(db, "r") as json_file:
        data = json.load(json_file)

    return getBaseFromDict(data)


def getBaseFromDict(data: dict) -> dict:

    dic = {}
    # Iterate over the outer dictionary

    for key, inner_dict in data.items():

        if str(type(inner_dict)) == "<class 'float'>":
            continue
        # Check if the key str(len(HintSet.operators)) exists in the inner dictionary
        if str(2**len(HintSet.operators)-1) in inner_dict:
            value = inner_dict[str(2**len(HintSet.operators)-1)]
        elif 2**len(HintSet.operators)-1 in inner_dict:
            value = inner_dict[2**len(HintSet.operators)-1]
        else:
            value = 300
        dic[key] = value

    return dic


def getSpeedupReal(base: dict, query: str, val: float):
    return base[query] - val


def getSpeedupFactor(base: dict, query: str, val: float):
    return (base[query] / val)


def calcSpeedups(db: str):
    job_base = getBase(db)

    with open(db, "r") as json_file:
        data = json.load(json_file)

    speedups = {}
    total_speedup_perc = 0
    total_speedup_abs = 0
    count = 0
    pg_def = 0
    for key, inner_dict in data.items():
        if str(type(inner_dict)) == "<class 'float'>":
            continue
        if "63" in inner_dict:
            pg_def += inner_dict["63"]
        else:
            pg_def += 300
        if not (inner_dict["opt"]):
            best = None
            speedupPerc = 100

        else:
            best = inner_dict[str(inner_dict["opt"])]
            speedupPerc = getSpeedupFactor(
                job_base, key, best)
            speedupAbs = getSpeedupReal(
                job_base, key, best)

        total_speedup_abs += speedupAbs
        total_speedup_perc += speedupPerc
        count += 1
        speedups[key] = {"speedup": speedupPerc,
                         "speedupAbs": speedupAbs, "opt": inner_dict["opt"]}

    speedups["avrgTOT"] = {"speedup": total_speedup_perc /
                           (count), "speedupAbs": total_speedup_abs, "speedupAvg": total_speedup_abs/count, "pg_def": pg_def}

    # Calculate average speedup for each best value
    average_speedups = calcAvgSpeedup(speedups)

    speedups["avrgTOT"]["runtime"] = data["runtime"]
    speedups["avrgTOT"]["factor"] = speedups["avrgTOT"]["speedupAbs"] / \
        data["runtime"]

    for key, inner_dict in average_speedups.items():
        speedups[key] = inner_dict

    return speedups


def calcAvgSpeedup(speedups: dict) -> dict:
    average_speedups = {}
    for key, inner_dict in speedups.items():

        if "opt" not in inner_dict:
            continue
        best = inner_dict["opt"]
        speedup = inner_dict["speedup"]
        if best not in average_speedups:
            average_speedups[best] = {"total_speedup": 0, "count": 0}
        average_speedups[best]["total_speedup"] += speedup
        average_speedups[best]["count"] += 1

    for best, data in average_speedups.items():
        average_speedup = data["total_speedup"] / data["count"]
        average_speedups[best]["average_speedup"] = average_speedup

    return average_speedups


def speedup(context):
    with open(context.split(".json")[0]+"_speedup.json", "w") as json_file:
        data = json.dump(fp=json_file, obj=calcSpeedups(context))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate physical operator labels for input queries and save to json")

    parser.add_argument("context", default=None,
                        help="File in which queries results are located")
    args = parser.parse_args()
    speedup(args.context)
    # with open("output/JOB_out.json", "w") as json_file:
    #     data = json.dump(fp=json_file, obj=calcSpeedupsJob())
    # print(calcSpeedupsJob())

    # with open("output/TPCH_out.json", "w") as json_file:
    #     data = json.dump(fp=json_file, obj=calcSpeedups("TPCH"))
    # print(calcSpeedups("TPCH"))
