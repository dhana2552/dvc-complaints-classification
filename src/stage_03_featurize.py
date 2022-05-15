import argparse
import os
import logging
from utils.common import read_yaml, create_directories
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from utils.featurize import clean_text
from sklearn.model_selection import train_test_split
import numpy as np

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
    train_dir_path = os.path.join(featurized_data_dir_path, artifacts["TRAIN_DIR"])
    test_dir_path = os.path.join(featurized_data_dir_path, artifacts["TEST_DIR"])
    create_directories([train_dir_path])
    create_directories([test_dir_path])
    X_train_data = os.path.join(train_dir_path, artifacts["X_TRAIN_DATA"])
    y_train_data = os.path.join(train_dir_path, artifacts["Y_TRAIN_DATA"])
    X_test_data = os.path.join(test_dir_path, artifacts["X_TEST_DATA"])
    y_test_data = os.path.join(test_dir_path, artifacts["Y_TEST_DATA"])
    
       
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
    
    X = df.complaints    
    y = df.product_id
    
    split = params["featurize"]["split"]
    seed = params["featurize"]["seed"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split, random_state=seed)
    X_train = bag_of_words.fit_transform(X_train)
    X_train = tfidf.fit_transform(X_train).toarray()
    X_test = bag_of_words.transform(X_test)
    X_test = tfidf.transform(X_test).toarray()

    np.save(X_train_data, X_train)
    np.save(y_train_data, y_train)
    np.save(X_test_data, X_test)
    np.save(y_test_data, y_test)
    

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