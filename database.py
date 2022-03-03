import mysql.connector.pooling
import json


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

# for api/attractions


def search_attracion(**data):
    start = (int(data['page']))*12
    if data['keyword']:
        sql = f"SELECT * FROM attractions WHERE name LIKE '%{data['keyword']}%' LIMIT {start},12"

    else:
        sql = f"SELECT * FROM attractions LIMIT {start}, 12" 
        

    mycursor.execute(sql)
    result = mycursor.fetchall()
    if result:
        list = []
        for i in result:
            item = dict(zip(mycursor.column_names, i))
            item ["images"] = json.loads(item["images"])
            list.append(item)
        return list
    else:
        return None

def search_attractionid(data):
    id=data
    sql=f"SELECT * FROM attractions WHERE id = {id}"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for i in result:
        item = dict(zip(mycursor.column_names, i))
        item ["images"] = json.loads(item["images"])
  
       
        return item
    else:
        return None
search_attractionid(2)

