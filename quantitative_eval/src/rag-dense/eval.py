import argparse
import os
import scipy.stats
import sys
import json
import pytrec_eval


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('qrel')
    parser.add_argument('run', nargs=1)

    # A bit too strict, as it does not allow for parametrized measures,
    # but sufficient for the example.
#    parser.add_argument('--measure',
 #                       choices=pytrec_eval.supported_measures,
 #                       required=True)
    measures = {'recip_rank','ndcg_cut_5', 'ndcg_cut_10', 'ndcg'}

    args = parser.parse_args()

    assert os.path.exists(args.qrel)
    assert all(map(os.path.exists, args.run))

    with open(args.qrel, 'r') as f_qrel:
        qrel = pytrec_eval.parse_qrel(f_qrel)

    with open(args.run[0], 'r') as f_run:
        first_run = pytrec_eval.parse_run(f_run)

   # with open(args.run[1], 'r') as f_run:
   #     second_run = pytrec_eval.parse_run(f_run)

    evaluator = pytrec_eval.RelevanceEvaluator(
        qrel, measures)

    first_results = evaluator.evaluate(first_run)
    print(json.dumps(first_results, indent=True))

    #avg_recip_rank = sum([first_results[query_id]['recip_rank'] for query_id in first_results.keys()]) / len(first_results.keys())
    #avg_ndcg = sum([first_results[query_id]['ndcg'] for query_id in first_results.keys()]) / len(first_results.keys())
    

    averages = {}
    for measure in measures:
        avg_measure = sum([first_results[query_id][measure] for query_id in first_results.keys()]) / len(first_results.keys())
        averages[measure] = avg_measure


    latex_table = """
  {0} & RR & {1:.2f} \\\\
  nDCG & {2:.2f} \\\\
  nDCG@5 & {3:.2f} \\\\
  nDCG@10 & {4:.2f} \\\\
  \\hline
""".format(args.run[0], averages['recip_rank'], averages['ndcg'], averages['ndcg_cut_5'], averages['ndcg_cut_10'])

    # Print or save the LaTeX table
    print(latex_table)

    
    #second_results = evaluator.evaluate(second_run)

    #query_ids = list(
    #    set(first_results.keys()) & set(second_results.keys()))

    #first_scores = [
    #    first_results[query_id][args.measure] for query_id in query_ids]
    #second_scores = [
    #    second_results[query_id][args.measure] for query_id in query_ids]

    #print(scipy.stats.ttest_rel(first_scores, second_scores))

if __name__ == "__main__":
    sys.exit(main())