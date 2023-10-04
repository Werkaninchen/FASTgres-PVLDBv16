import json
from hint_sets import HintSet


def getBase(db: str) -> dict:
    with open("output/test_"+db+"_single_off.json", "r") as json_file:
        data = json.load(json_file)

    return getBaseFromDict(data)


def getBaseFromDict(data: dict) -> dict:

    dic = {}
    # Iterate over the outer dictionary
    for key, inner_dict in data.items():
        # Check if the key str(len(HintSet.operators)) exists in the inner dictionary
        if str(len(HintSet.operators)) in inner_dict:
            value = inner_dict[str(len(HintSet.operators))]
        else:
            value = 300
        dic[key] = value

    return dic


def getSpeedup(base: dict, query: str, val: float):
    # print(base)
    return base[query] / val


def calcSpeedups(db: str):
    job_base = getBase(db)

    with open("output/test_"+db+"_single_on.json", "r") as json_file:
        data = json.load(json_file)

    speedups = {}
    total_speedup = 0
    count = 0
    for key, inner_dict in data.items():
        if not (inner_dict["opt"]):
            best = None
            speedup = 100

        else:
            best = inner_dict[str(inner_dict["opt"])]
            speedup = getSpeedup(
                job_base, key, best)
        key += "_ON"
        total_speedup += speedup
        count += 1
        speedups[key] = {"speedup": speedup, "opt": inner_dict["opt"]}

    with open("output/test_"+db+"_single_off.json", "r") as json_file:
        data = json.load(json_file)

    total_speedup_off = 0
    count_off = 0
    for key, inner_dict in data.items():
        best = inner_dict[str(inner_dict["opt"])]
        speedup = getSpeedup(
            job_base, key, best)
        key += "_OFF"
        total_speedup_off += speedup
        count_off += 1
        speedups[key] = {"speedup": speedup, "opt": inner_dict["opt"]}

    speedups["avrgON"] = {"speedup": total_speedup/count}
    speedups["avrgOFF"] = {"speedup": total_speedup_off/count_off}

    speedups["avrgTOT"] = {"speedup": (
        total_speedup_off+total_speedup)/(count_off+count)}

    # Calculate average speedup for each best value
    average_speedups = calcAvgSpeedup(speedups)

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


if __name__ == "__main__":

    context = "STACK_10"

    # with open("output/JOB_out.json", "w") as json_file:
    #     data = json.dump(fp=json_file, obj=calcSpeedupsJob())
    # print(calcSpeedupsJob())

    # with open("output/TPCH_out.json", "w") as json_file:
    #     data = json.dump(fp=json_file, obj=calcSpeedups("TPCH"))
    # print(calcSpeedups("TPCH"))

    with open("output/"+context+"_out.json", "w") as json_file:
        data = json.dump(fp=json_file, obj=calcSpeedups(context))
    print(calcSpeedups(context))
