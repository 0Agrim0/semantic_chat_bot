import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()


def get_sql_data(query: str):
    mydb = mysql.connector.connect(
        host=os.getenv('SQL_IP'),
        user=os.getenv('SQL_USER'),
        password=os.getenv('SQL_PASSWORD')
    )

    mycursor = mydb.cursor()
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    mycursor.close()
    return myresult


def get_sql_dataframe(query: str):
    mydb = mysql.connector.connect(
        host=os.getenv('SQL_IP'),
        user=os.getenv('SQL_USER'),
        password=os.getenv('SQL_PASSWORD')
    )

    df_mysql = pd.read_sql(sql=query, con=mydb)
    return df_mysql
