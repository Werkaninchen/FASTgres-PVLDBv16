import utility as u
from hint_sets import HintSet
import generate_labels as gl
import speedup

import random
import statistics
import math


def run_heuristic(path, save, conn_str, strategy, query_dict,  static_timeout: bool, reduced: bool, single: bool):
    queries = u.get_queries(path)

    random.shuffle(queries)
    # run for all hints on (default)

    # speedup to default > 2 -> remove hint
    # standard timeout of 5 minutes should suffice as pg opt is at max 2.2 minutes on other evals
    # hintList = [i for i in range(2 ** len(HintSet.operators))]

    hint_list = [2**i for i in range(len(HintSet.operators))]
    # hint_list = [1024, 4, 64, 2]
    old_list = []
    n = 0
    print("Using heuristic evaluation")
    for i in range(len(queries)):
        query = queries[i]
        try:
            # Check if we can skip queries
            opt_val = query_dict[query]['opt']
            print("Found optimum for query {}, {}".format(query, opt_val))
            continue
        except KeyError:
            # Evaluate like default
            pass
        print('\nEvaluating query: {}, {} / {}'.format(query, i+1, len(queries)))

        if not 2**len(HintSet.operators)-1 in hint_list:
            hint_list.append((2**len(HintSet.operators))-1)

        query_dict = gl.get_best_hint_single(
            path, query, conn_str, query_dict, reduced, hint_list)
        if 2**len(HintSet.operators)-1 in hint_list:
            hint_list.remove((2**len(HintSet.operators))-1)
        if strategy == 'strict':
            print('\nSaving evaluation')
            u.save_json(query_dict, save)
        elif strategy == 'interval':
            if i % 20 == 0:
                print('\nSaving evaluation')
                u.save_json(query_dict, save)

        # remove hints every 10 iterations, 3 is not fixed yet
        if i > 0 and i % 10 == 0:
            hint_list = removeHints(query_dict, hint_list)

        stable, old_list, n = hintsAreStable(hint_list, old_list, n)
        # break early to allow combinations of hint in next step
        if stable or len(hint_list) <= 5:
            break
        hint_list = orderBySpeed(query_dict, hint_list)
    print('\nSaving evaluation')
    u.save_json(query_dict, save)
    # TODO: decide if calling remove hints is advantageous
    # run for combinations
    # Take best hints and combine them 2d
    new_hint_list = []
    max_run_time = {}
    for i in range(len(queries)):

        max = 300

        if str(2**len(HintSet.operators)-1) in query_dict[queries[i]]:
            max = query_dict[queries[i]][str(
                2**len(HintSet.operators)-1)]
        if 2**len(HintSet.operators)-1 in query_dict[queries[i]]:
            max = query_dict[queries[i]][
                2**len(HintSet.operators)-1]

        for idx in hint_list:
            for idx2 in hint_list:

                if (idx + idx2) in [2**i for i in range(len(HintSet.operators))]:
                    continue

                if (idx + idx2) >= 2**len(HintSet.operators):
                    continue
                # set timeout to best run

                if queries[i] in max_run_time:
                    max = max_run_time[queries[i]]
                a = 300
                b = 300

                if str(idx) in query_dict[queries[i]]:
                    a = query_dict[queries[i]][str(idx)]
                if str(idx2) in query_dict[queries[i]]:
                    b = query_dict[queries[i]][str(idx2)]
                if idx in query_dict[queries[i]]:
                    a = query_dict[queries[i]][idx]
                if idx2 in query_dict[queries[i]]:
                    b = query_dict[queries[i]][idx2]
                max_run_time[queries[i]] = min(max, a, b)
                new_hint_list.append(idx+idx2)

    hint_list = list(set(new_hint_list))

    for i in range(len(queries)):
        query = queries[i]
        # hint list already orderd by speed because of line 40
        print('\nEvaluating query: {}, {} / {}'.format(query, i+1, len(queries)))

        query_dict = gl.get_best_hint_single(
            path, query, conn_str, query_dict, reduced, hint_list, max_run_time[queries[i]])

        if strategy == 'strict':
            print('\nSaving evaluation')
            u.save_json(query_dict, save)
        elif strategy == 'interval':
            if i % 20 == 0:
                print('\nSaving evaluation')
                u.save_json(query_dict, save)
        if i > 0 and i % 10 == 0:
            hint_list = removeHints(query_dict, hint_list)

        stable, old_list, n = hintsAreStable(hint_list, old_list, n)
        if stable:
            break

        hint_list = orderBySpeed(query_dict, hint_list)

    # TODO run the reast of the queries by combination
    # TODO test if list is stable/ a good improvement is already found


def orderBySpeed(query_dict: dict, hint_list: list):

    new_hint_set = {}
    # iterate over queries
    base_dict = speedup.getBaseFromDict(query_dict)
    for queryIdx in query_dict:

        for i in hint_list:
            if not i in new_hint_set:
                new_hint_set[i] = {"improvement": 0, "n": 0}

            if not i in query_dict[queryIdx]:
                continue

            improvement = speedup.getSpeedup(
                base_dict, queryIdx, query_dict[queryIdx][i])

            new_hint_set[i] = {
                "improvement": new_hint_set[i]["improvement"]+improvement, "n": new_hint_set[i]["n"]+1}
    new_hint_list = []
    for i in new_hint_set.keys():
        new_hint_list.append(i)

    new_hint_list.sort(
        # dont reverse, list is reveresd on runtime
        key=lambda x: new_hint_set[x]["improvement"] / max(1, new_hint_set[x]["n"]), reverse=False)

    return new_hint_list


# this might never be true if we have alternating query "types"

def hintsAreStable(hint_list: list, old_list: list, n: int):
    if old_list != hint_list:
        return (False, hint_list, 0)
    # stable if hint list didn't change for more than n iterations
    if n >= 10:
        return (True, old_list, n+1)
    return (False, old_list, n+1)


# all of these will be improvements over base as it's checked first and then used as timeout
def removeHints(query_dict: dict, hint_list: list):
    print("removing hints")

    if len(hint_list) < 5:
        print("no hints removed")
        return hint_list

    # hint list is already sorted by speedup per occurance

    new_hint_set = {}

    base_dict = speedup.getBaseFromDict(query_dict)

    # sum up hint occurence over queries
    for queryIdx in query_dict:
        for i in hint_list:
            if not i in query_dict[queryIdx]:
                continue
            if not i in new_hint_set:
                new_hint_set[i] = {
                    "n": 1, "speedup": base_dict[queryIdx] / query_dict[queryIdx][i]}
            else:
                new_hint_set[i] = {"n": new_hint_set[i]["n"]+1,
                                   "speedup":  new_hint_set[i]["speedup"] + base_dict[queryIdx] / query_dict[queryIdx][i]}
    new_hint_list = []

    # purge hint if it doesn't meet limit
    # TODO new limit calculation

    speedups = []
    for i in new_hint_set:
        if new_hint_set[i]["n"] == 0:
            continue
        speedups.append(new_hint_set[i]["speedup"]/new_hint_set[i]["n"])

    print(speedups)
    limit = statistics.mean(speedups)
    print(statistics.stdev(speedups))
    # if statistics.stdev(speedups) > 1
    for el in new_hint_set:
        if new_hint_set[el]["speedup"] >= limit:
            new_hint_list.append(el)
    if new_hint_list == []:
        return hint_list

    print(new_hint_list)
    return new_hint_list


if __name__ == "__main__":
    query_dict = u.load_json("output/test_STACK_10_single_on_heur_l4_2d.json")
    hint_list = [2**i for i in range(len(HintSet.operators))]
    print(hint_list)
    hint_list = removeHints(query_dict, hint_list)
    print(hint_list)
    hint_list = orderBySpeed(query_dict, hint_list)
    print(hint_list)
