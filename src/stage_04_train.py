import argparse
import os
import logging
from utils.common import read_yaml, create_directories
import pandas as pd
from sklearn.svm import SVC
import numpy as np
import joblib

STAGE = "stage 04 train"

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(config_path):
    ## read config files
    config = read_yaml(config_path)
    
    artifacts = config["artifacts"]
    featurized_data_dir_path = os.path.join(artifacts["ARTIFACTS_DIR"], artifacts["FEATURIZED_DIR"])
    train_dir_path = os.path.join(featurized_data_dir_path, artifacts["TRAIN_DIR"])
    X_train_data = os.path.join(train_dir_path, artifacts["X_TRAIN_DATA"])
    y_train_data = os.path.join(train_dir_path, artifacts["Y_TRAIN_DATA"])
    model_dir_path = os.path.join(artifacts["ARTIFACTS_DIR"], artifacts["MODEL_DIR"])
    create_directories([model_dir_path])
    model = os.path.join(model_dir_path, artifacts["MODEL_NAME"])
    
    X_train = np.load(X_train_data)
    y_train = np.load(y_train_data)
    
    svc = SVC()
    svc.fit(X_train, y_train)
    joblib.dump(svc, model)
    


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e