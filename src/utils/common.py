import os
import yaml
import logging
import json
from io import BytesIO, TextIOWrapper
from zipfile import ZipFile
import urllib.request as req
import joblib
import warnings
warnings.filterwarnings("ignore")

def read_yaml(path_to_yaml: str) -> dict:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    logging.info(f"yaml file: {path_to_yaml} loaded successfully")
    return content

def create_directories(path_to_directories: list) -> None:
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        logging.info(f"created directory at: {path}")


def save_json(path: str, data: dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    logging.info(f"json file saved at: {path}")
    
def download_zip(url: str, zip_file: str, file_name: str) -> None:
    logging.info(f"downloading data from: {url}")
    zipped_data = req.urlopen(url+ req.quote(zip_file))
    zip_file = ZipFile(BytesIO(zipped_data.read()))
    logging.info(f"data downloaded successfully")
    data = TextIOWrapper(zip_file.open(file_name), encoding='utf-8')
    return data

def reduce_product(df, product):
    #considering only the first 1000 records from each product for a balance in dataset
    df_reduced = df[df.products == product].head(1000)
    logging.info("Picked only top 1000 records from each product for a balance in dataset")
    return df_reduced

def save_file(result, out_path):
    logging.info(f"Saving file to: {out_path}")
    joblib.dump(result, out_path)
    logging.info(f"File saved successfully")