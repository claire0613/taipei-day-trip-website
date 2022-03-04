import mysql.connector.pooling


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
mycursor.execute("""
CREATE TABLE IF NOT EXISTS attractions(
id BIGINT AUTO_INCREMENT, name VARCHAR(255) NOT NULL, category VARCHAR(255) NOT NULL, 
description TEXT NOT NULL, address VARCHAR(255) NOT NULL, transport TEXT, 
mrt VARCHAR(255), latitude DOUBLE NOT NULL, longitude DOUBLE NOT NULL, 
images JSON NOT NULL,
PRIMARY KEY (id))ENGINE=InnoDB; 
    """)  # InnoDB 儲存引擎 具備Commit, Rollback和當掉復原的事務處理能力，可保護使用者資料
connection.commit()
