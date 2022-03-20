import mysql.connector.pooling
from mysql.connector import Error
import json
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
def connection_db(sql,value):
    try:
        connection = connection_pool.get_connection()
        mycursor = connection.cursor()
        mycursor.execute(sql, value)
        
    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)

    finally:
        result=mycursor.fetchall()
        if connection.in_transaction:
            connection.rollback()
        mycursor.close()
        connection.close()
        return result


# for api/attractions

def attraction_count(**data):
    if data['keyword']:
        sql="SELECT count(name) FROM attractions WHERE name LIKE %s "
        value=('%'+data['keyword']+'%',)
    
    else:
        sql="SELECT count(name) FROM attractions"
        value=()
    allcount=connection_db(sql,value)
  
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
    result = connection_db(sql,value)
    if result:
        lst = []
        for i in result:
            item=resultformat(i)
            lst.append(item)
        return lst
    else:
        return None

def resultformat(result):
    result = {
        "id":result[0],
        "name":result[1],
        "category":result[2],
        "description":result[3],
        "address":result[4],
        "transport":result[5],
        "mrt":result[6],
        "latitude":result[7],
        "longitude":result[8],
        "images":json.loads(result[9])
    }
    return result


def search_attractionid(data):
  
    sql="SELECT * FROM attractions WHERE id = %s"
    value=(data,)
    result =  connection_db(sql,value)
    if result:
        for i in result:
            item=resultformat(i)
        return item
    else:
        return None
    

