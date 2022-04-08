
import mysql.connector.pooling
import os
from dotenv import load_dotenv
load_dotenv()


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
mycursor.execute("""
CREATE TABLE IF NOT EXISTS attractions(
id BIGINT AUTO_INCREMENT, name VARCHAR(255) NOT NULL, category VARCHAR(255) NOT NULL, 
description TEXT NOT NULL, address VARCHAR(255) NOT NULL, transport TEXT, 
mrt VARCHAR(255), latitude DOUBLE NOT NULL, longitude DOUBLE NOT NULL, 
images JSON NOT NULL,
PRIMARY KEY (id))ENGINE=InnoDB; 
    """)  # InnoDB 儲存引擎 具備Commit, Rollback和當掉復原的事務處理能力，可保護使用者資料

mycursor.execute("""
   CREATE TABLE IF NOT EXISTS users(
      id BIGINT  AUTO_INCREMENT,
      name VARCHAR(255) NOT NULL, 
      email VARCHAR(255) NOT NULL UNIQUE, 
      password VARCHAR(255) NOT NULL, 
      PRIMARY KEY (id)) charset=utf8;
   """
)

mycursor.execute("""
   CREATE TABLE IF NOT EXISTS bookings(
    id BIGINT NOT NULL AUTO_INCREMENT, 
    attractionId INT NOT NULL, 
    userId BIGINT NOT NULL, 
    date DATE NOT NULL, 
    time VARCHAR(255) NOT NULL, 
    price INT NOT NULL,
    status INT DEFAULT 1,
    totalPrice INT ,
    ordernum varchar(255) DEFAULT NULL,
    rec_trade_id VARCHAR(255)DEFAULT NULL,
    phone VARCHAR(255),
    PRIMARY KEY(id),
    FOREIGN KEY(userId)REFERENCES users(id)ON DELETE CASCADE) charset=utf8;
   """
)

connection.commit()




