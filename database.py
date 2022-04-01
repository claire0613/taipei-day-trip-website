import mysql.connector.pooling
from mysql.connector import Error
import json
import os
from datetime import datetime, timedelta
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
        connection.commit()
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
    
    

# for api/users


def search_users(email,password=None):
    if password:
        sql="SELECT * FROM users WHERE email = %s and password = %s"
        value=(email,password)
    else: 
        sql="SELECT * FROM users WHERE email = %s "
        value=(email,)
    result=connection_db(sql,value)

    if result:
            return {
        "id":result[0][0],
        "name":result[0][1],
        "email":result[0][2],
        }
    else:
        return None
    
def insert_user(**data):
    sql = "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)"
    value=(data['name'],data['email'],data['password'])
    result=connection_db(sql,value)
    if result:
        return True
    return None


# for /api/booking
def search_booking(user_id):
    sql="""SELECT a.id, a.name, a.address, a.images, b.date, b.time, b.price 
            FROM bookings as b JOIN attractions as a ON b.attractionId = a.id WHERE b.userId=%s"""
    value=(user_id,)
    result=connection_db(sql,value)
    if result:
        return {
            "id": result[0][0],
            "name": result[0][1],
            "address":result[0][2],
            "image":json.loads(result[0][3])[0],
            "date": result[0][4],
            "time": result[0][5],
            "price": result[0][6]
            }
        
    else:
        return None
def insert_booking(user_id, attraction_id, date, time, price):
    sql="SELECT * FROM bookings WHERE userId=%s"
    value=(user_id,)
    has_user_booking=connection_db(sql,value)
    if has_user_booking==[]:
        sql="INSERT INTO bookings (userId, attractionId, date, time, price) VALUE (%s,%s,%s,%s,%s)"
        value=(user_id, attraction_id, date, time, price)
        result=connection_db(sql,value)
    else:
        sql="UPDATE bookings SET attractionId =%s, date=%s, time=%s, price=%s WHERE userId=%s"
        value=(attraction_id, date, time, price,user_id)
        result=connection_db(sql,value)
        
def remove_booking(user_id):
    sql="DELETE FROM bookings WHERE userId=%s"
    value=(user_id,)
    result=connection_db(sql,value)
    if result:
        return True
    return None


# search_users(email='333@gmail.com',password='333')
# print(search_booking(user_id=8))
# insert_booking(user_id=8, attraction_id=2, date='2022-04-04', time="morning", price=2000)