import mysql.connector
import mysql.connector.pooling
from mysql.connector import Error
import json
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


        



# for api/attractions

def attraction_count(**data):
    if data['keyword']:
        sql="SELECT count(name) FROM attractions WHERE name LIKE %s "
        value=('%'+data['keyword']+'%',)
        mycursor.execute(sql,value)
    
    else:
        sql="SELECT count(name) FROM attractions"
        mycursor.execute(sql)
        
    allcount=mycursor.fetchall()
  
    if  allcount:
        return  int(allcount[0][0])


def search_attracion(**data):
    page_12 = int(data["page"])*12
    if data['keyword']:
        sql = "SELECT * FROM attractions WHERE name LIKE %s LIMIT %s, %s"
        value=('%'+data['keyword']+'%',page_12,12)
    else:
        sql = "SELECT * FROM attractions LIMIT %s , %s" 
        value=(page_12,12)
    mycursor.execute(sql,value)
    result = mycursor.fetchall()
    if result:
        lst = []
        for i in result:
            item = dict(zip(mycursor.column_names, i))
            item ["images"] = json.loads(item["images"])
            lst.append(item)
        return lst
    else:
        return None




def search_attractionid(data):
  
    sql="SELECT * FROM attractions WHERE id = %s"
    value=(data,)
    mycursor.execute(sql,value)
    result = mycursor.fetchall()
    for i in result:
        item = dict(zip(mycursor.column_names, i))
        item ["images"] = json.loads(item["images"])

        return item
    else:
        return None
    
    
