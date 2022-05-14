import argparse
import os
import logging
from utils.common import read_yaml, create_directories
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from utils.featurize import clean_text


STAGE = "stage 03 featurize"

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(config_path, params_path):
    ## read config files
    config = read_yaml(config_path)
    params = read_yaml(params_path)
    
    artifacts = config["artifacts"]
    prepared_data_dir_path = os.path.join(artifacts["ARTIFACTS_DIR"], artifacts["PREPARED_DIR"])
    prepared_data = os.path.join(prepared_data_dir_path, artifacts["PREPARED_DATA"])
    featurized_data_dir_path = os.path.join(artifacts["ARTIFACTS_DIR"], artifacts["FEATURIZED_DIR"])
    create_directories([featurized_data_dir_path])
    featurized_data = os.path.join(featurized_data_dir_path, artifacts["FEATURIZED_DATA"])
    
       
    max_features = params["featurize"]["max_features"]
    n_grams = params["featurize"]["ngrams"]
    le = LabelEncoder()
    bag_of_words = CountVectorizer(
        stop_words="english",
        max_features=max_features,
        ngram_range=(1, n_grams)
    )  
    tfidf = TfidfTransformer()
    
    df = pd.read_pickle(prepared_data)
    df['product_id'] = le.fit_transform(df.products)
    df.complaints = clean_text(df.complaints)
    df.complaints = df.complaints.apply(lambda x: bag_of_words.fit_transform(x))
    df.complaints = df.complaints.apply(lambda x: tfidf.fit_transform(x).toarray())
    df.to_pickle(featurized_data)
    

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config, params_path=parsed_args.params)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e