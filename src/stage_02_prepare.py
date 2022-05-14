import argparse
import os
import logging
from utils.common import read_yaml, reduce_product, create_directories
from utils.db_mgmt import connect_db
import pandas as pd


STAGE = "stage 02 prepare"

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
    prepared_data_dir_path = os.path.join(artifacts["ARTIFACTS_DIR"], artifacts["PREPARED_DIR"])
    create_directories([prepared_data_dir_path])
    prepared_data = os.path.join(prepared_data_dir_path, artifacts["PREPARED_DATA"])
    
    #db path
    local_data_dir = config["source_download_dir"]["data_dir"]
    db_name = config["source_download_dir"]["data_db"]
    table_name = config["source_download_dir"]["data_table"]
    db_path = os.path.join(local_data_dir, db_name)
   
    cnx = connect_db(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", con=cnx)
    logging.info(f"The shape of data frame is {df.shape}")
    print(df.head())
    
    #Removing aggregated products
    df.drop(df[df.products == 'Credit reporting, credit repair services, or other personal consumer reports'].index, inplace=True)
    df.drop(df[df.products == 'Money transfer, virtual currency, or money service'].index, inplace=True)
    df.drop(df[df.products == 'Payday loan, title loan, or personal loan'].index, inplace=True)
    df.drop(df[df.products == 'Credit card or prepaid card'].index, inplace=True)
    logging.info(f"The shape of data frame after removing aggregated products is {df.shape}")
    
    ## Combining Loans together to make this a simplier classification problem
    df.replace('Student loan', 'Loan', inplace=True)
    df.replace('Consumer Loan', 'Loan', inplace=True)
    df.replace('Payday loan', 'Loan', inplace=True)
    df.replace('Vehicle loan or lease', 'Loan', inplace=True)
    # Placing Virtual currency into other financial service
    df.replace('Virtual currency', 'other services', inplace=True)
    df.replace("Other financial service", 'other services', inplace=True)
    df.replace('Checking or savings account', 'savings account', inplace=True)
    df.replace('Bank account or service', 'savings account', inplace=True)
    logging.info(f"Renamed and grouped product categories to {df.products.nunique()}")
    
    product_categories = df.products.unique()
    df_filtered = pd.DataFrame()
    for product in product_categories:
        df_filtered = df_filtered.append(reduce_product(df, product))
    df_filtered.reset_index(drop=True, inplace=True)
    logging.info(f"Created a new dataframe with filtered data {df_filtered.shape}")
    
    #Save to dir
    df_filtered.to_pickle(prepared_data)
    

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