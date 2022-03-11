import mysql.connector.pooling
from mysql.connector import Error
import os
from dotenv import load_dotenv
load_dotenv()
try:
    dbconfig = {
        'host': os.getenv("SERVER_HOST"),
        'user': os.getenv("SERVER_USER"),
        'password': os.getenv("SERVER_PASSWORD"),
        'database': os.getenv("SERVER_DATABSE"),
        'charset': 'utf8',
        
    }

    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="pool",
        pool_size=5,
        pool_reset_session=True,
        **dbconfig
    )
    connection = connection_pool.get_connection()
    mycursor = connection.cursor()


except Error as e:
    print("Error while connecting to MySQL using Connection pool ", e)

finally:
    if connection.in_transaction:
        connection.rollback()
    mycursor.close()
    connection.close()
