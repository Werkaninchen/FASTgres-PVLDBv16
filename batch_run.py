import generate_labels
import heuristic_run
import autosteer_eval
import utility as u
import os


def run_rel():
    timeouts = {
        "JOB": 300,
        "TPC-H": 300,
    }
    for i in range(110, 250, 10):
        context = "TPC-H"
        threshold = i/100
        print("running for threshold", threshold)
        path = "queries/tpch/"

        qs = u.get_queries(path)
        query_eval_dict = dict(zip(qs, [dict() for _ in range(len(qs))]))

        savepath = "output/threshold" + \
            str(threshold) + "/"
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        savepath += context+"_old.json"
        heuristic_run.run_heuristic(
            path, save=savepath, conn_str=u.PG_TPC_H, strategy="interval", query_dict=query_eval_dict, static_timeout=False, reduced=False, single=False, threshold=threshold, timeout=timeouts[context])

    # for i in range(15, 40, 5):
        context = "JOB"
        threshold = i/100
        print("running for threshold", threshold)
        path = "queries/job_queries/"

        qs = u.get_queries(path)
        query_eval_dict = dict(zip(qs, [dict() for _ in range(len(qs))]))

        savepath = "output/threshold" + \
            str(threshold) + "/"
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        savepath += context+"_old.json"
        heuristic_run.run_heuristic(
            path, save=savepath, conn_str=u.PG_IMDB, strategy="interval", query_dict=query_eval_dict, static_timeout=False, reduced=False, single=False, threshold=threshold, timeout=timeouts[context])

    # for i in range(15, 40, 5):
    #     context = "Stack"
    #     threshold = i/10
    #     print("running for threshold", threshold)
    #     path = "queries/stack/context_10/"

    #     qs = u.get_queries(path)
    #     query_eval_dict = dict(zip(qs, [dict() for _ in range(len(qs))]))

    #     savepath = "output/threshold" + \
    #         str(threshold) + "/"
    #     if not os.path.exists(savepath):
    #         os.makedirs(savepath)
    #     savepath += context+"_old.json"
    #     heuristic_run.run_heuristic(
    #         path, save=savepath, conn_str=u.PG_TPC_H, strategy="interval", query_dict=query_eval_dict, static_timeout=False, reduced=False, single=False, threshold=threshold)


def run_abs():

    items = range(2, 18, 4)

    for i in items:
        context = "TPC-H"
        threshold = i
        print("running for threshold", threshold)
        path = "queries/tpch/"

        qs = u.get_queries(path)
        query_eval_dict = dict(zip(qs, [dict() for _ in range(len(qs))]))

        savepath = "output/threshold" + \
            str(threshold) + "/"
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        savepath += context+"_old.json"
        heuristic_run.run_heuristic(
            path, save=savepath, conn_str=u.PG_TPC_H, strategy="interval", query_dict=query_eval_dict, static_timeout=False, reduced=False, single=False, threshold=threshold)

    # for i in items:
        context = "JOB"
        threshold = i
        print("running for threshold", threshold)
        path = "queries/job_queries/"

        qs = u.get_queries(path)
        query_eval_dict = dict(zip(qs, [dict() for _ in range(len(qs))]))

        savepath = "output/threshold" + \
            str(threshold) + "/"
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        savepath += context+"_old.json"
        heuristic_run.run_heuristic(
            path, save=savepath, conn_str=u.PG_IMDB, strategy="interval", query_dict=query_eval_dict, static_timeout=False, reduced=False, single=False, threshold=threshold)

    # for i in range(15, 40, 5):
    #     context = "Stack"
    #     print("running for threshold", threshold)
    #     path = "queries/stack/context_10/"

    #     qs = u.get_queries(path)
    #     query_eval_dict = dict(zip(qs, [dict() for _ in range(len(qs))]))

    #     savepath = "output/threshold" + \
    #         str(threshold) + "/"
    #     if not os.path.exists(savepath):
    #         os.makedirs(savepath)
    #     savepath += context+"_old.json"
    #     heuristic_run.run_heuristic(
    #         path, save=savepath, conn_str=u.PG_TPC_H, strategy="interval", query_dict=query_eval_dict, static_timeout=False, reduced=False, single=False, threshold=threshold)


def run_autosteer():
    context = "TPC-H"

    print("running autosteer for TPC-H")
    path = "queries/tpch/"

    qs = u.get_queries(path)
    query_eval_dict = dict(zip(qs, [dict() for _ in range(len(qs))]))

    savepath = "output/autosteer/"
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    savepath += context+"_old.json"
    autosteer_eval.run_autosteer(
        path, save=savepath, conn_str=u.PG_TPC_H, strategy="interval", query_dict=query_eval_dict, static_timeout=False, reduced=False, single=False, threshold=300)

    context = "JOB"

    print("running autosteer for JOB")
    path = "queries/job_queries/"

    qs = u.get_queries(path)
    query_eval_dict = dict(zip(qs, [dict() for _ in range(len(qs))]))

    savepath = "output/autosteer/"
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    savepath += context+"_old.json"
    autosteer_eval.run_autosteer(
        path, save=savepath, conn_str=u.PG_IMDB, strategy="interval", query_dict=query_eval_dict, static_timeout=False, reduced=False, single=False, threshold=300)


if __name__ == "__main__":
    run_autosteer()
