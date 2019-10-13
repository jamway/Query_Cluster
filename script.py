from bqtools import bqclient
from preprocess import text_preprocessor
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pandas as pd
import logging
from datetime import datetime, timezone
import os


def main():
    path_to_cred = ""
    project_id = env.PROJECT_ID
    job_id = env.JOB_ID
    deployment_id = job_id
    query = env.QUERY
    start_time=datetime.time()
    bq = bqclient(path_to_cred, project_id)
    logging.getLogger().setLevel(logging.DEBUG)
    log_output=logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level='INFO')
    message = {
            "job_id": job_id,
            "name": deployment_id,
            "project_id": project_id,
            "status": "STARTED",
            "start_time": start_time,
            "end_time": datetime.now(timezone.utc).isoformat(),
            "log_output": log_output
        }
    bq.publish_message(message, "topic")
    try:
        df = text_preprocessor(bq.query_data(query)).post_df
        documents = []
        for row_n in range(len(df)):
            documents.append(TaggedDocument(df.iloc[row_n][1], [df.iloc[row_n][0]]))
            if row_n > 9:
                break
        model = Doc2Vec(documents, vector_size=200, window=10, dm=1, dbow_words=0, min_count=1, workers=1)
        model.save(f"./model/{project_id}")
        
        vector_df = pd.DataFrame( {'vector': [list(model.docvecs[i]) for i in range(len(model.docvecs))] } )
        df['vector'] = df.iloc[[1]].apply(list(model.infer_vector))
    except Exception as err:
        print(err)
        logging.debug(str(err))
        message = {
            "job_id": job_id,
            "name": deployment_id,
            "project_id": project_id,
            "status": "FAILED",
            "start_time": start_time,
            "end_time": datetime.now(timezone.utc).isoformat(),
            "log_output": str(err)
        }
        bq.publish_message(message, "topic")
   




if __name__ == "__main__":
    main()
