from pyserini.search import FaissSearcher
from pyserini import trectools
from pyserini.output_writer import OutputFormat, get_output_writer

import pandas as pd

DATA_DIR = "../../data"

COLLECTION = DATA_DIR + "/collection.csv"
TOPICS = DATA_DIR + "/topics.csv"
GROUNDTRUTH = DATA_DIR + "/groundtruth.csv"
INDEX="../../target/indexes/tct_colbert-v2-hnp-msmarco-faiss"

OUTPUT_PATH = '../../target/runs/rag-dense-faiss.txt'

QUERY_ENCODER = 'facebook/dpr-question_encoder-multiset-base'

topics = pd.read_csv(TOPICS)

searcher = FaissSearcher(
    INDEX,
    QUERY_ENCODER
)

num_hits = 100


tag = "walert.rag.dense.faiss"

output_writer = get_output_writer(OUTPUT_PATH, OutputFormat('trec'), 'w',
                                      max_hits=num_hits, tag=tag, topics=topics)
with output_writer:
        batch_topics = list()
        batch_topic_ids = list()
        for question_id, question in topics[['question_id','question']].values:
            hits = searcher.search(question, num_hits)
            results = [(question_id, hits)]
            
            for question_id, hits in results:
                output_writer.write(question_id, hits)

            results.clear()
