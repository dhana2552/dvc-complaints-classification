import logging
import sqlite3

def connect_db(db_path: str) -> str:
    try:
        conn = sqlite3.connect(db_path)
        logging.info(f"Connected to {db_path}")
    except:
        logging.error(f"Failed to connect to {db_path}")
    return conn

def create_table(db_path, table_name, values):
    try:
        conn = connect_db(db_path)
        conn.execute(f"CREATE TABLE {table_name} ({values})")
        logging.info(f"Created table {table_name}")
    except:
        logging.error(f"Failed to create table {table_name}")
        
def insert_data(db_path, table_name, values):
    try:
        conn = connect_db(db_path)
        conn.execute(f"INSERT INTO {table_name} VALUES ({values})")
        logging.info(f"Inserted data into {table_name}")
    except:
        logging.error(f"Failed to insert data into {table_name}")
        
def drop_table(db_path, table_name):
    try:
        conn = connect_db(db_path)
        conn.execute(f"DROP TABLE {table_name}")
        logging.info(f"Dropped table {table_name}")
    except:
        logging.error(f"Failed to drop table {table_name}")
        
def delete_all_data(db_path, table_name, values):
    try:
        conn = connect_db(db_path)
        conn.execute(f"DELETE FROM {table_name}")
        conn.close()
        logging.info(f"Deleted all data from {table_name}")
    except:
        create_table(db_path, table_name, values)
        conn.close()
        logging.info(f"Created the table {table_name} as the table doesn't exist")