
# Builds query labels by grid search

import argparse
import itertools
import os
import speedup

import numpy as np
import heuristic_run
import utility as u
from hint_set import HintSet
from tqdm import tqdm


def get_best_hint_single_static(path, query, conn_str, query_dict, reduced):

    iteration_list = []

    for i in range(len(HintSet.operators)):
        iteration_list.append(2**i)
    # PG default
    timeout = u.evaluate_hinted_query(path, query, HintSet(32), conn_str, 300)
    if timeout == None:
        timeout = 200
    best_hint_time = timeout
    best_hint = 32

    hint_set_evaluations = query_dict[query]
    hint_set_evaluations["32"] = timeout
    query_dict[query] = hint_set_evaluations
    # timeout factor
    timeout = timeout * 1.5

    print("Evaluating Hint Set List: {}".format(iteration_list))

    for j in reversed(iteration_list):
        print("Evaluating Hint Set {}".format(j))
        if j in query_dict[query]:
            print('Found query entry')
            query_hint_time = query_dict[query][j]
            if query_hint_time < best_hint_time:
                best_hint = j
                best_hint_time = query_hint_time
            continue
        else:
            print('Evaluating Query')
            query_hint_time = u.evaluate_hinted_query(
                path, query, HintSet(j), conn_str, timeout)

        if query_hint_time is None:
            hint_set_evaluations = query_dict[query]
            hint_set_evaluations[j] = timeout
            query_dict[query] = hint_set_evaluations
            print("Setting query: {} to time: {}".format(query, timeout))
        else:
            hint_set_evaluations = query_dict[query]
            hint_set_evaluations[j] = query_hint_time
            query_dict[query] = hint_set_evaluations
            if query_hint_time < best_hint_time:
                best_hint = j
                best_hint_time = query_hint_time
                print("Setting best hint to: {}".format(best_hint))
            print("Setting query: {} to time: {}".format(query, query_hint_time))

    query_dict[query]['opt'] = best_hint
    return query_dict


def excedesSpeedTheshhold(query_dict: dict, queryIdx: str, hintSet: int, threshhold: float):
    base_dict = speedup.getBaseFromDict(query_dict)

    if queryIdx == 2 ** len(HintSet.operators)-1:
        return False

    improvement = speedup.getSpeedupPerc(
        base_dict, queryIdx, query_dict[queryIdx][hintSet])
    print(improvement)
    return improvement >= threshhold


def excedesSpeedTheshholdAbs(query_dict: dict, queryIdx: str, hintSet: int, threshhold: float):
    base_dict = speedup.getBaseFromDict(query_dict)

    if queryIdx == 2 ** len(HintSet.operators)-1:
        return False

    improvement = speedup.getSpeedupReal(
        base_dict, queryIdx, query_dict[queryIdx][hintSet])
    print(improvement)
    return improvement >= threshhold


def get_best_hint_single(path, query, conn_str, query_dict, reduced, hint_override=[], timeout=300, threshold=1000):
    # standard timeout of 5 minutes should suffice as pg opt is at max 2.2 minutes on other evals
    best_hint = None

    if reduced:
        to_switch_off = [32, 16, 8]
        iteration_list = list(sorted(get_combinations(to_switch_off)))
        iteration_list = [int(_) for _ in iteration_list]
    elif hint_override != []:
        iteration_list = hint_override
    # else:
    #     iteration_list = [((2**len(HintSet.operators))-1) - (2**i)
    #                       for i in range(len(HintSet.operators))]

    #     # add base case all on
    #     iteration_list.append((2**len(HintSet.operators))-1)

    else:
        iteration_list = [2**i for i in range(len(HintSet.operators))]

    for hint_set_int in reversed(iteration_list):
        print("Evaluating Hint Set {}".format(hint_set_int))
        if str(hint_set_int) in query_dict[query].keys():
            print('Found query entry')
            query_hint_time = query_dict[query][str(hint_set_int)]

            if timeout is None or query_hint_time < timeout:
                timeout = query_hint_time
                best_hint = hint_set_int
            else:
                print('Found query but timed out')
            continue
        else:
            hint_set = HintSet(hint_set_int)
            query_hint_time = u.evaluate_hinted_query(
                path, query, hint_set, conn_str, timeout)

        if query_hint_time is None:
            # timed out queries can not be counted
            print('Timed out query')
            continue

            # update dictionary

        query_dict[query][hint_set_int] = query_hint_time

        # update timeout
        if timeout is None or query_hint_time < timeout:
            timeout = query_hint_time
            best_hint = hint_set_int

        print('Adjusted Timeout with Query: {}, Hint Set: {}, Time: {}'
              .format(query, u.int_to_binary(hint_set_int), query_hint_time))
        # if faster than 1.5x base break
        if excedesSpeedTheshhold(query_dict=query_dict, queryIdx=query, hintSet=hint_set_int, threshhold=threshold):
            print("exceded ", threshold, "x threshold")
            break
    query_dict[query]['opt'] = best_hint
    return query_dict


def get_combinations(to_switch_off: list):
    temp = {1: True, 0: False}
    bin_comb = list(itertools.product([0, 1], repeat=len(to_switch_off)))
    bool_comb = [[temp[_[i]] for i in range(len(_))] for _ in bin_comb]
    combinations = list()
    for comb in bool_comb:
        combinations.append(63 - sum(np.array(to_switch_off)[np.array(comb)]))
    return combinations


def get_best_hint_set_static(path, query, conn_str, query_dict, reduced):
    # PG default
    timeout = u.evaluate_hinted_query(path, query, HintSet(63), conn_str, None)
    best_hint_time = timeout
    best_hint = 63

    hint_set_evaluations = query_dict[query]
    hint_set_evaluations["63"] = timeout
    query_dict[query] = hint_set_evaluations
    # timeout factor
    timeout = 1.5 * timeout

    for j in range(2 ** len(HintSet.operators)-1):
        j = (2 ** len(HintSet.operators) - 2) - j
        print("Evaluating Hint Set {}/ {}".format(j,
              (2 ** len(HintSet.operators)) - 2))
        if j in query_dict[query]:
            print('Found query entry')
            query_hint_time = query_dict[query][j]
            if query_hint_time < best_hint_time:
                best_hint = j
                best_hint_time = query_hint_time
            continue
        else:
            print('Evaluating Query')
            query_hint_time = u.evaluate_hinted_query(
                path, query, HintSet(j), conn_str, timeout)

        if query_hint_time is None:
            hint_set_evaluations = query_dict[query]
            hint_set_evaluations[j] = timeout
            query_dict[query] = hint_set_evaluations
            print("Setting query: {} to time: {}".format(query, timeout))
        else:
            hint_set_evaluations = query_dict[query]
            hint_set_evaluations[j] = query_hint_time
            query_dict[query] = hint_set_evaluations
            if query_hint_time < best_hint_time:
                best_hint = j
                best_hint_time = query_hint_time
                print("Setting best hint to: {}".format(best_hint))
            print("Setting query: {} to time: {}".format(query, query_hint_time))

    query_dict[query]['opt'] = best_hint
    return query_dict


def get_best_hint_set_et(path, query, conn_str, query_dict, reduced):
    # standard timeout of 5 minutes should suffice as pg opt is at max 2.2 minutes on other evals
    timeout = 300
    best_hint = None

    if reduced:
        to_switch_off = [32, 16, 8]
        iteration_list = list(sorted(get_combinations(to_switch_off)))
        iteration_list = [int(_) for _ in iteration_list]
    else:
        iteration_list = [i for i in range(2 ** len(HintSet.operators))]

    for hint_set_int in reversed(iteration_list):
        print("Evaluating Hint Set {}".format(hint_set_int))
        if hint_set_int in query_dict[query].keys():
            print('Found query entry')
            query_hint_time = query_dict[query][hint_set_int]
            if timeout is None or query_hint_time < timeout:
                timeout = query_hint_time
                best_hint = hint_set_int
            print('Found query but timed out')
            continue
        else:
            print('Evaluating Query')
            hint_set = HintSet(hint_set_int)
            query_hint_time = u.evaluate_hinted_query(
                path, query, hint_set, conn_str, timeout)

        if query_hint_time is None:
            # timed out queries can not be counted
            print('Timed out query')
            continue
        else:
            # update dictionary
            hint_set_evaluations = query_dict[query]
            hint_set_evaluations[hint_set_int] = query_hint_time
            query_dict[query] = hint_set_evaluations

            # update timeout
            if timeout is None or query_hint_time < timeout:
                timeout = query_hint_time
                best_hint = hint_set_int

        print('Adjusted Timeout with Query: {}, Hint Set: {}, Time: {}'
              .format(query, u.int_to_binary(hint_set_int), query_hint_time))
    query_dict[query]['opt'] = best_hint
    return query_dict


def get_best_hint_set(path, query, conn_str, query_dict, reduced):
    # standard timeout of 5 minutes should suffice as pg opt is at max 2.2 minutes on other evals
    timeout = 300
    best_hint = None

    if reduced:
        to_switch_off = [32, 16, 8]
        iteration_list = list(sorted(get_combinations(to_switch_off)))
        iteration_list = [int(_) for _ in iteration_list]
    else:
        iteration_list = [i for i in range(2 ** len(HintSet.operators))]

    for hint_set_int in reversed(iteration_list):
        print("Evaluating Hint Set {}".format(hint_set_int))
        if hint_set_int in query_dict[query].keys():
            print('Found query entry')
            query_hint_time = query_dict[query][hint_set_int]
            if timeout is None or query_hint_time < timeout:
                timeout = query_hint_time
                best_hint = hint_set_int
            print('Found query but timed out')
            continue
        else:
            print('Evaluating Query')
            hint_set = HintSet(hint_set_int)
            query_hint_time = u.evaluate_hinted_query(
                path, query, hint_set, conn_str, timeout)

        if query_hint_time is None:
            # timed out queries can not be counted
            print('Timed out query')
            continue
        else:
            # update dictionary
            hint_set_evaluations = query_dict[query]
            hint_set_evaluations[hint_set_int] = query_hint_time
            query_dict[query] = hint_set_evaluations

            # update timeout
            if timeout is None or query_hint_time < timeout:
                timeout = query_hint_time
                best_hint = hint_set_int

        print('Adjusted Timeout with Query: {}, Hint Set: {}, Time: {}'
              .format(query, u.int_to_binary(hint_set_int), query_hint_time))
    query_dict[query]['opt'] = best_hint
    return query_dict


def run(path, save, conn_str, strategy, query_dict,  static_timeout: bool, reduced: bool, single: bool):
    queries = u.get_queries(path)
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

        if static_timeout:
            print("Using static evaluation")
            if single:
                query_dict = get_best_hint_single_static(
                    path, query, conn_str, query_dict, reduced)
            else:
                query_dict = get_best_hint_set_static(
                    path, query, conn_str, query_dict, reduced)
        else:
            if single:
                query_dict = get_best_hint_single(
                    path, query, conn_str, query_dict, reduced)
            else:
                query_dict = get_best_hint_set(
                    path, query, conn_str, query_dict, reduced)

        if strategy == 'strict':
            print('\nSaving evaluation')
            u.save_json(query_dict, save)
        elif strategy == 'interval':
            if i % 20 == 0:
                print('\nSaving evaluation')
                u.save_json(query_dict, save)

    print('\nFinal saving')
    u.save_json(query_dict, save)
    return


def main():
    print("Using label gen version 1.08 - Reduced Support, Standard Timeout 5min")
    parser = argparse.ArgumentParser(
        description="Generate physical operator labels for input queries and save to json")
    parser.add_argument("queries", default=None,
                        help="Directory in which .sql-queries are located")
    parser.add_argument("-o", "--output", default=None,
                        help="Output dictionary save name")
    parser.add_argument("-s", "--strategy", default="interval", help="Save strategy during evaluation, strict will save"
                        " after each adjustment, interval after a certain "
                                                                     "amount of adjustments, and lazy at the end of "
                                                                     "the evaluation. Lazy is not recommended as there"
                                                                     " may be a substantial loss of data upon "
                                                                     "encountering unexpected errors.")
    parser.add_argument("-1", "--single", default="interval",
                        help="use single hints only.")
    parser.add_argument("-db", "--database", default=None,
                        help="Database string in psycopg2 format.")
    parser.add_argument("-c", "--complete", default=False, help="Builds result dictionary using a static timeout of "
                                                                "1.5 times the pg default execution time.")
    parser.add_argument("-r", "--reduced", default=False,
                        help="Info to use reduced hints")
    args = parser.parse_args()

    query_path = args.queries
    save_path = args.output
    evaluation_strategy = args.strategy
    args_db_string = args.database
    if args_db_string == "imdb":
        args_db_string = u.PG_IMDB
    elif args_db_string == "job":
        args_db_string = u.PG_IMDB
    elif args_db_string == "stack":
        args_db_string = u.PG_STACK_OVERFLOW
    elif args_db_string == "stack-2016":
        args_db_string = u.PG_STACK_OVERFLOW_REDUCED_16
    elif args_db_string == "stack-2013":
        args_db_string = u.PG_STACK_OVERFLOW_REDUCED_13
    elif args_db_string == "stack-2010":
        args_db_string = u.PG_STACK_OVERFLOW_REDUCED_10
    elif args_db_string == "tpch":
        args_db_string = u.PG_TPC_H

    if query_path is None:
        raise argparse.ArgumentError(args.queries, "No query path provided")

    if save_path is None:
        raise argparse.ArgumentError(args.queries, "No output path provided")
    elif os.path.exists(save_path):
        print("Loading existing Evaluation Dict")
        query_eval_dict = u.load_json(save_path)
    else:
        # initialize dict over all queries
        print("Creating new Evaluation Dict")
        qs = u.get_queries(query_path)
        query_eval_dict = dict(zip(qs, [dict() for _ in range(len(qs))]))

    if evaluation_strategy not in ['strict', 'interval', 'lazy']:
        raise ValueError('Evaluation strategy not recognized')

    args_complete = args.complete

    # if args_complete not in ["True", "False"]:
    #     raise ValueError(
    #         "Complete evaluation option only takes boolean values.")
    args_complete = True if args_complete == "True" else False
    arg_reduced = True if args.reduced == "True" else False

    if arg_reduced:
        print('Using reduced sets - 3 joins')
    if args_complete:
        print('Using complete Evaluation')

    arg_single = True if args.single == "True" else False

    if arg_reduced:
        print('Using sigle hints')
    connection_string = args_db_string

    # run(query_path, save_path, connection_string, evaluation_strategy,
    #     query_eval_dict, args_complete, arg_reduced, arg_single)

    heuristic_run.run_heuristic(query_path, save_path, connection_string, evaluation_strategy,
                                query_eval_dict, args_complete, arg_reduced, arg_single)

    print("Finished Label Generation")


if __name__ == "__main__":

    main()
