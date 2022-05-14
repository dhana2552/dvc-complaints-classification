import argparse
import os
import logging
from utils.common import read_yaml, download_zip, create_directories
from utils.db_mgmt import connect_db, drop_table
import pandas as pd


STAGE = "stage 01 get and ingest data"

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(config_path):
    ## read config files
    config = read_yaml(config_path)
    cf_url = config["source_data_url"]["CF_URL"]
    zip_ext = config["source_data_url"]["ZIP_EXTENSION"]
    csv_file = config["source_data_url"]["CSV_IN_ZIP"]
    
    ##Create db folder
    local_data_dir = config["source_download_dir"]["data_dir"]
    db_name = config["source_download_dir"]["data_db"]
    table_name = config["source_download_dir"]["data_table"]
    create_directories([local_data_dir])
    db_path = os.path.join(local_data_dir, db_name)
    
    #Only Product and Consumer complaint narrative are needed
    df = pd.read_csv(download_zip(cf_url, zip_ext, csv_file))
    df = df[['Product', 'Consumer complaint narrative']]
    logging.info(f"The shape of data frame is {df.shape}")
    
    #Remove null values
    df.dropna(axis=0, inplace=True)
    logging.info(f"The shape of data frame after removing null values is {df.shape}")
    
    #Remove duplicates
    logging.info(f"Number of duplicates in df is {df.duplicated().sum()} with total shape {df.shape}")
    df.drop_duplicates(inplace=True)
    logging.info(f"The shape of data frame after removing duplicates is {df.shape}")
    
    #Renaming the columns
    df.rename(columns={'Product': 'products', 'Consumer complaint narrative': 'complaints'}, inplace=True)
    df.reset_index(drop=True, inplace=True)
    logging.info(f"Columns renamed as {df.columns} successfully")
    
    #Saving dataframe to sqlite
    drop_table(db_path, table_name)
    cnx = connect_db(db_path)
    df.to_sql(table_name, cnx, index=False)
    logging.info(f"Dataframe saved to sqlite successfully")

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