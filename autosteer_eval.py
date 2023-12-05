import generate_labels
from hint_set import HintSet
import utility as u
import time


def combine_hints(hint_set_1: int, hint_set_list: list):
    # combine hints to hint sets
    return list(set([hint_set_1 | hint_set_2[0] for hint_set_2 in hint_set_list]))


def run_autosteer(path, save, conn_str, strategy, query_dict,  static_timeout: bool, reduced: bool, single: bool, threshold: float):
    queries = u.get_queries(path)

    # random.shuffle(queries)
    # run for all hints on (default)

    # speedup to default > 2 -> remove hint
    # standard timeout of 5 minutes should suffice as pg opt is at max 2.2 minutes on other evals
    # hintList = [i for i in range(2 ** len(HintSet.operators))]

    hint_list = [i for i in range(2 ** len(HintSet.operators))]
    # hint_list = [1024, 4, 64, 2]
    old_list = []
    n = 0
    print("Using heuristic evaluation")
    start = time.time()
    for i in range(len(queries)):

        query = queries[i]

        print('\nEvaluating query: {}, {} / {}'.format(query, i+1, len(queries)))

        query_dict = get_best_hint_autosteer(
            path, query, conn_str, query_dict, reduced, threshold=threshold)

        if strategy == 'strict':
            print('\nSaving evaluation')
            u.save_json(query_dict, save)
        elif strategy == 'interval':
            if i % 20 == 0:
                print('\nSaving evaluation')
                u.save_json(query_dict, save)

    end = time.time()
    query_dict["runtime"] = end-start
    u.save_json(query_dict, save)


def get_best_hint_autosteer(path, query, conn_str, query_dict, reduced, timeout=300.0, threshold=1000, thresholAbs=1000):
    # standard timeout of 5 minutes should suffice as pg opt is at max 2.2 minutes on other evals

    singleton_hint_sets = []
    best_hint = 2**len(HintSet.operators)-1
    print("Evaluating Hint Set {}".format(best_hint))
    pg_default = u.evaluate_hinted_query(
        path, query,  HintSet(2**len(HintSet.operators)-1), conn_str, timeout)

    best_hint = 2**len(HintSet.operators)-1
    best_time = pg_default
    print('Adjusted Timeout with Query: {}, Hint Set: {}, Time: {}'
          .format(query, u.int_to_binary(best_hint), pg_default))

    iteration_list = []
    iteration_list = [best_hint - (2**i)
                      for i in range(len(HintSet.operators))]
    print(iteration_list)

    for hint_set_int in reversed(iteration_list):
        print("Evaluating Hint Set {}".format(hint_set_int))

        hint_set = HintSet(hint_set_int)
        query_hint_time = u.evaluate_hinted_query(
            path, query, hint_set, conn_str, pg_default)

        if query_hint_time is None:
            # timed out queries can not be counted
            print('Timed out query')
            continue

        # update dictionary

        query_dict[query][hint_set_int] = query_hint_time

        if best_time is not None and query_hint_time < best_time:
            best_hint = hint_set_int
            best_time = query_hint_time

        # update timeout
        if pg_default is None or query_hint_time < pg_default:
            singleton_hint_sets.append((hint_set_int, query_hint_time))

        print('Adjusted Timeout with Query: {}, Hint Set: {}, Time: {}'
              .format(query, u.int_to_binary(hint_set_int), query_hint_time))

    hint_sets = [i[0] for i in singleton_hint_sets]
    while len(hint_sets) >= 1:
        hint_set = HintSet(hint_sets.pop())
        combined_hs = combine_hints(
            hint_set.get_int_name(), singleton_hint_sets)
        for hint_set_int in combined_hs:
            print("Evaluating Hint Set {}".format(hint_set_int))

            query_hint_time = u.evaluate_hinted_query(
                path, query, HintSet(hint_set_int), conn_str, pg_default)

            if query_hint_time is None:
                # timed out queries can not be counted
                print('Timed out query')
                continue

            # update dictionary

            query_dict[query][hint_set_int] = query_hint_time
            if query_hint_time < best_time:
                best_hint = hint_set_int
                best_time = query_hint_time
            # update timeout
            if timeout is None or query_hint_time < pg_default:
                singleton_hint_sets.append((hint_set_int, query_hint_time))

            print('Adjusted Timeout with Query: {}, Hint Set: {}, Time: {}'
                  .format(query, u.int_to_binary(hint_set_int), query_hint_time))

    # combine hints to hint sets

    query_dict["singelton_hints"] = singleton_hint_sets

    query_dict[query]['opt'] = best_hint
    return query_dict
