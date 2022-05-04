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


def search_users(email):
    
    sql="SELECT * FROM users WHERE email = %s "
    value=(email,)
    result=connection_db(sql,value)

    if result:
            return {
        "id":result[0][0],
        "name":result[0][1],
        "email":result[0][2],
        "password":result[0][3]
        }
    else:
        return None
    
def insert_user(name,email,password):
    sql="SELECT * FROM users WHERE email=%s"
    value=(email,)
    is_email_existing=connection_db(sql,value)
    if is_email_existing==[]:
        sql = "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)"
        value=(name,email,password)
        result=connection_db(sql,value)
        return True
    return None



# for /api/booking
def search_booking(user_id):
    sql="""SELECT b.id,a.id, a.name, a.address, a.images, b.date, b.time, b.price 
            FROM bookings as b JOIN attractions as a ON b.attractionId = a.id WHERE b.userId=%s and ordernum IS NULL"""
    value=(user_id,)
    results=connection_db(sql,value)
    result_list=[]

    if results:
        for result in results:
            data={
            "bookingId":result[0],
            "attractionId": result[1],
            "name": result[2],
            "address":result[3],
            "image":json.loads(result[4])[0],
            "date": result[5],
            "time": result[6],
            "price": result[7]
            }
            result_list.append(data)
        return result_list
        
    else:
        return None
def insert_booking(user_id, attraction_id, date, time, price):
    
    sql="INSERT INTO bookings (userId, attractionId, date, time, price) VALUE (%s,%s,%s,%s,%s)"
    value=(user_id, attraction_id, date, time, price)
    result=connection_db(sql,value)

        
def remove_booking(booking_id):
    try:
        sql="DELETE FROM bookings WHERE id=%s"
        value=(booking_id,)
        result=connection_db(sql,value)
        return True
    except:
        return None


# print(insert_user(name='2222',email='2222@gmail.com',password='2222'))
# search_users(email='333@gmail.com',password='333')
# print(search_booking(user_id=15))
# insert_booking(user_id=8, attraction_id=2, date='2022-04-04', time="morning", price=2000)
def update_booking_for_order(user_id,total_price,order_num,phone):
    try:
        sql='UPDATE bookings SET totalprice=%s,ordernum=%s,phone=%s WHERE userId=%s and ordernum IS NULL'
        value=(total_price,order_num,phone,user_id)
        result=connection_db(sql,value)
        return True
    except:
        return None


def update_booking_for_pay(order_num,status,rec_trade_id):
    try:
        sql='UPDATE bookings SET status=%s,rec_trade_id=%s WHERE ordernum=%s'
        value=(status,rec_trade_id,order_num)
        result=connection_db(sql,value)
        return True
    except:
        return None


def search_ordernum(order_num):
    try:
        
        sql="""SELECT b.id,a.id,a.name,a.address,a.images,b.date,b.time,b.price,b.totalPrice,
            b.ordernum,b.rec_trade_id,b.status,u.name,u.email,b.phone 
            FROM bookings as b LEFT JOIN (attractions as a, users as u) ON a.id=b.attractionId and u.id=b.userId WHERE ordernum=%s"""
        value=(order_num,)
        results=connection_db(sql,value)
        result_lst=[]
        if results:
            for result in results:
                data={
                    "bookingId":result[0],
                    "attractionId": result[1],
                    "name": result[2],
                    "address":result[3],
                    "image":json.loads(result[4])[0],
                    "date": result[5],
                    "time": result[6],
                    "price":result[7],
                    "totalPrice": result[8],
                    "ordernum":result[9],
                    "rec_trade_id":result[10],
                    "status":result[11],
                    "ordername":result[12],
                    "email":result[13],
                    "phone":result[14]
                    }
                result_lst.append(data)
                
            return result_lst
    except:
        return None
# for search_order_history
def search_order_history(user_id):
    
    sql="""SELECT a.name,b.date,b.time,b.price,b.totalPrice,
            b.ordernum,b.status 
            FROM bookings as b  JOIN attractions as a ON a.id=b.attractionId  WHERE userId=%s and ordernum IS NOT NULL;
        """
    value=(user_id,)
    results=connection_db(sql,value)
    if results:
        result_list=[]
        for result in results:
            data={
            "attractionName": result[0],
            "date": result[1],
            "time": result[2],
            "price": result[3],
            "totalPrice": result[4],
            "ordernum":result[5],
            "status":result[6],
        
            }
            result_list.append(data)
        return result_list
        
    else:
        return None

    
def updated_name_pwd(user_id=None,new_name=None,pwd=None):
    try:
        if new_name:
                sql="UPDATE  users SET name = %s WHERE id = %s"
                value=(new_name,user_id)
                result=connection_db(sql,value)
              
        elif pwd:
                sql="UPDATE  users SET password = %s WHERE id = %s"
                value=(pwd,user_id)
                result=connection_db(sql,value)
        return True
        
    except: 
        return None
