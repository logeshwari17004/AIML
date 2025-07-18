import os
import pandas as pd
import numpy as np
import logging
import mysql.connector
from sqlalchemy import create_engine

logging.basicConfig(filename='etl_process.log', level=logging.INFO)


def log_message(message):
    logging.info(message)


log_message("ETL process started.")
def extract_data(folder_path):
    data_frames = []
    for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            data_frames.append(df)
    combined_data = pd.concat(data_frames, ignore_index=True)
    log_message(f"Extracted {len(combined_data)} rows of data from CSV files.")
    return combined_data
folder_path = 'data/'  # Path to the data folder
sales_data = extract_data(folder_path)
log_message("Data extraction completed.")

def transform_data(df):
    df.fillna({
        'Quantity_Sold': 0,
        'Unit_Price': 0.0,
        'Discount_Percent': 0.0,
        'Payment_Mode': 'Cash'
    }, inplace=True)


    df['Total_Sale_Value'] = df['Quantity_Sold'] * df['Unit_Price'] * (1 - df['Discount_Percent'] / 100)


    df.columns = df.columns.str.lower()
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df.drop_duplicates(subset=['store_id', 'date', 'product_id'], inplace=True)
    df['sales_category'] = np.select(
        [
            df['total_sale_value'] >= 1000,  # High sales
            (df['total_sale_value'] < 1000) & (df['total_sale_value'] >= 500),  # Medium sales
            df['total_sale_value'] < 500  # Low sales
        ],
        ['High', 'Medium', 'Low'],
        default='Low'
    )

    log_message(f"Data transformation completed with {len(df)} rows.")
    return df


sales_data = transform_data(sales_data)

def load_to_mysql(df, db_name='retail_sales_db', table_name='retail_sales'):
    engine = create_engine(f'mysql+mysqlconnector://username:password@localhost/{db_name}')
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    log_message(f"Data loaded to MySQL table: {table_name}")

load_to_mysql(sales_data)



def generate_reports(df):
    store_sales = df.groupby('store_id')['total_sale_value'].sum().reset_index()

    top_5_products = df.groupby('product_name')['total_sale_value'].sum().nlargest(5).reset_index()
    daily_sales_trend = df.groupby(['store_id', 'date'])['total_sale_value'].sum().reset_index()

    store_sales.to_csv('store_sales_summary.csv', index=False)
    top_5_products.to_csv('top_5_products.csv', index=False)
    daily_sales_trend.to_csv('daily_sales_trend.csv', index=False)

    log_message("Analysis reports saved to CSV.")
generate_reports(sales_data)

log_message("ETL process completed successfully.")
