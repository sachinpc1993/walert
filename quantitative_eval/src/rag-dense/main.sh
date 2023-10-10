##1. Parse test collection:
#python data.py

##2. Encode test collection:
#./encode.sh

##3. Index test collection:
#./index.sh

##4. Run the searches:
#python search.py

##5. Evaluate the run:
#RAG Dense
python eval.py ../../data/qrels.txt ../../target/runs/rag-dense-faiss.txt > ../../target/trec_eval_results/rag-dense.tex
trec_eval -m all_trec -q ../../data/qrels.txt ../../target/runs/rag-dense-faiss.txt > ../../target/trec_eval_results/rag-dense.txt

#RAG BM25
python eval.py ../../data/qrels.txt ../../target/runs/rag-bm25.txt > ../../target/trec_eval_results/bm25.tex
trec_eval -m all_trec -q ../../data/qrels.txt ../../target/runs/rag-bm25.txt > ../../target/trec_eval_results/bm25.txt

#Intent-based
python eval.py ../../data/qrels.txt ../../target/runs/walert-intent.txt > ../../target/trec_eval_results/walert-intent.tex
trec_eval -m all_trec -q ../../data/qrels.txt ../../target/runs/walert-intent.txt > ../../target/trec_eval_results/walert-intent.txt