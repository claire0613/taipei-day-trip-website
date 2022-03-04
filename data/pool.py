import json
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

try:
    dbconfig = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'charset': 'utf8',
        'database': 'taipei_trip',
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
