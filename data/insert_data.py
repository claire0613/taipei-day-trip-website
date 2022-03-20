import json
import mysql.connector
import mysql.connector.pooling
from dotenv import load_dotenv
load_dotenv()
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


with open('data/taipei-attractions.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
attraction_list = data["result"]["results"]

for spot in attraction_list:
    images_cut = spot["file"].split('https')
    images = []
    for i in range(1, len(images_cut)):
        if images_cut[i].find('.jpg')!= -1 or images_cut[i].find('.JPG')!= -1 or images_cut[i].find('.png')!= -1 \
            or images_cut[i].find('.PNG')!= -1 :
            images.append('https'+images_cut[i])
        
            
    sql = ("INSERT INTO attractions"
           "(name,category,description,address,transport,mrt,latitude,longitude,images)"
           "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    value = spot['stitle'], spot['CAT2'], spot['xbody'], spot['address'], spot[
        'info'], spot['MRT'], spot['latitude'], spot['longitude'], json.dumps(images)
    mycursor.execute(sql, value)
    connection.commit()
