import generate_labels
import heuristic_run
import utility as u
import os
if __name__ == "__main__":
    for i in range(15, 40, 5):
        context = "TPC-H"
        threshold = i/10
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

    for i in range(15, 40, 5):
        context = "JOB"
        threshold = i/10
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

    for i in range(15, 40, 5):
        context = "Stack"
        threshold = i/10
        print("running for threshold", threshold)
        path = "queries/stack/context_10/"

        qs = u.get_queries(path)
        query_eval_dict = dict(zip(qs, [dict() for _ in range(len(qs))]))

        savepath = "output/threshold" + \
            str(threshold) + "/"
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        savepath += context+"_old.json"
        heuristic_run.run_heuristic(
            path, save=savepath, conn_str=u.PG_TPC_H, strategy="interval", query_dict=query_eval_dict, static_timeout=False, reduced=False, single=False, threshold=threshold)
