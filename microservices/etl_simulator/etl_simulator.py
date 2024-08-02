import pandas as pd
from sqlalchemy import create_engine, text
from os import getenv
from logging import getLogger

logger = getLogger(__name__)

features = pd.read_csv("database/features_dataset.csv")

DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_NAME = getenv("DB_NAME")

connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(connection_string)

with engine.connect() as connection:
    connection.execute(text("""
    CREATE TABLE IF NOT EXISTS features_dataset (
        date_block_num INT,
        shop_id INT,
        item_id INT,
        item_cnt_month_sum_lag_1 FLOAT,
        item_cnt_month_sum_lag_2 FLOAT,
        item_cnt_month_sum_lag_3 FLOAT,
        sales_proceeds_month_sum_lag_1 FLOAT,
        sales_proceeds_month_sum_lag_2 FLOAT,
        sales_proceeds_month_sum_lag_3 FLOAT,
        item_cnt_month_mean_lag_1 FLOAT,
        item_cnt_month_mean_lag_2 FLOAT,
        item_cnt_month_mean_lag_3 FLOAT,
        item_price_month_mean_lag_1 FLOAT,
        item_price_month_mean_lag_2 FLOAT,
        item_price_month_mean_lag_3 FLOAT,
        date_block_shop_mean_lag_1 FLOAT,
        date_block_shop_mean_lag_2 FLOAT,
        date_block_shop_mean_lag_3 FLOAT,
        date_block_item_mean_lag_1 FLOAT,
        date_block_item_mean_lag_2 FLOAT,
        date_block_item_mean_lag_3 FLOAT,
        date_block_category_mean_lag_1 FLOAT,
        date_block_category_mean_lag_2 FLOAT,
        date_block_category_mean_lag_3 FLOAT,
        lag_mean FLOAT,
        lag_std FLOAT,
        lag_min FLOAT,
        lag_max FLOAT,
        item_category_id_encoded INT,
        month_encoded INT,
        PRIMARY KEY (shop_id, item_id)
    );
    """))

features.to_sql("features_dataset", engine, if_exists="replace", index=False)