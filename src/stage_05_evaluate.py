import argparse
import os
import logging
from utils.common import read_yaml, save_json
import joblib
from sklearn.metrics import accuracy_score
import numpy as np


STAGE = "stage 05 evaluate"

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
    test_dir_path = os.path.join(featurized_data_dir_path, artifacts["TEST_DIR"]) 
    X_test_data = os.path.join(test_dir_path, artifacts["X_TEST_DATA"])
    y_test_data = os.path.join(test_dir_path, artifacts["Y_TEST_DATA"])
    model_dir_path = os.path.join(artifacts["ARTIFACTS_DIR"], artifacts["MODEL_DIR"])
    model_path = os.path.join(model_dir_path, artifacts["MODEL_NAME"])
    
    scores_json_path = config["metrics"]["SCORES"]
    
    X_test = np.load(X_test_data)
    y_test = np.load(y_test_data)
    model = joblib.load(model_path)
    
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    scores = {
        "accuracy": accuracy,
    }
    
    save_json(scores_json_path, scores)


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