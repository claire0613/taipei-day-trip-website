import re
from flask import Blueprint, session, request, jsonify
import requests,json,jwt,os
from datetime import datetime
from database import search_order_history, search_ordernum, update_booking_for_order, update_booking_for_pay,search_booking
from dotenv import load_dotenv
load_dotenv()

api_orders=Blueprint('api_orders',__name__)
partner_key=os.getenv("partner_key")

@api_orders.route('/order/<orderNumber>',methods=["GET"])
def get_order(orderNumber):
    try:
        search_order=search_ordernum(orderNumber)
        if search_order:
            trip_list=[]
            for trip in search_order:
                data={
                "attraction":
                    {
                        "id":trip["attractionId"],
                        "name": trip["name"],
                        "address":trip["address"],
                        "image":trip["image"]
                    },
                    "date": datetime.strftime(trip["date"], "%Y-%m-%d"),
                    "time":trip["time"],
                    "price":trip["price"],
                    }
                trip_list.append(data)
            order={
                    "data": {
                    "number": orderNumber,
                    "totalPrice": search_order[0]["totalPrice"],
                    "trip": trip_list,
                    "contact": {
                    "name":search_order[0]["ordername"],
                    "email": search_order[0]["email"],
                    "phone": search_order[0]["phone"]
                    },
                    "status": search_order[0]["status"]
                    }
                }
            return jsonify(order)
        else:
            return jsonify({"error":True,"message":"無此訂單"})
    except:
        return jsonify({"error":True,"message":"伺服器內部錯誤"})        
  
@api_orders.route('/orders',methods=['POST'])
def post_order():
    try:
        token_cookie=request.cookies.get('user_cookie')
        if token_cookie :
            user=jwt.decode(token_cookie,os.getenv("SECRET_KEY"),algorithms=['HS256'])
            user_id=user["id"]
            order=request.json 
            prime=order['prime']
            total_price=int(order['order']['price'])
            name=order['order']['contact']['name']
            email=order['order']['contact']['email']
            phone=order['order']['contact']['phone']
            order_num=datetime.now().strftime('%Y%m%d%H%M%S%f')+str(user["id"])
            checkprice=0
            
            #從資料庫比對訂購行程的總價格
            bookings=search_booking(user_id=user_id)
            if bookings:
                for booking in bookings:
                    checkprice+=booking["price"]
            
            #當訂單中沒有input內容or使用者更動總價格等輸入不正確的狀況
            
            if (prime == None) or (checkprice != total_price) or (name == None) or (email == None)\
                or  not bool(re.match(r"\A09[0-9]{8}\b", phone)):
                data = {
                    "error": True,
                    "message": "訂單建立失敗，輸入不正確或其他原因"
                }
                return jsonify(data)
            else:
                #更新資料庫 加入訂單編號以及總價格
                updateorder=update_booking_for_order(user_id,total_price,order_num,phone)
                if updateorder:
                    post_data={
                        "prime":prime,
                        "partner_key":partner_key,
                        "merchant_id": "claire0613_CTBC",
                        "details":"台北一日遊行程付款",
                        "amount": 1,
                        "currency": "TWD",
                        "cardholder": {
                            "phone_number": phone,
                            "name": name,
                            "email": email,
                        },
                        "order_num": order_num,
                        "remember": True
                    }
                    pay_url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
                    headers = {
                    'Content-type': 'application/json',
                    'x-api-key': partner_key
                    }
                    
                    #給request到tappay伺服器進行付款
                    response = requests.post(pay_url, data=json.dumps(post_data), headers=headers)
                    res = response.json()
                    status=res["status"]
                    if status==0:
                        rec_trade_id=res["rec_trade_id"]
                        update_status=update_booking_for_pay(order_num,status,rec_trade_id)
                        if update_status:
                            tappay={
                                    "data": {
                                    "number": order_num,
                                    "payment": {
                                    "status": status,
                                    "message": "付款成功"
                                    }
                                }
                            }
                        else:
                            tappay={
                                "error":True,
                                "message": {"details":"付款狀態更改失敗","number": order_num,}
                                }
                    else:
                        tappay={
                                "error":True,
                                "message": {"details":"付款失敗","number": order_num,}
                                }
                    return jsonify(tappay)
                
        else:
            return jsonify({"error":True,"message":"請先登入"})       
    except:
        return jsonify({"error": True, "message": "伺服器內部錯誤"})     

@api_orders.route('/orders',methods=['GET'])
def get_order_history():
    try:
        token_cookie=request.cookies.get('user_cookie')
        page = int(request.args.get('page'))
        if token_cookie:
            user=jwt.decode(token_cookie,os.getenv("SECRET_KEY"),algorithms=['HS256'])
            user_id=user["id"]
            orders_history=search_order_history(user_id)
            orders_dic={}
            orders_history_list=[]
            all_count=0
            if orders_history: 
            #製作[{"單號1":[景點1,景點2]},{"單號2":[景點1]},...]資料結構
                for trip in orders_history:
                    ordernum=trip["ordernum"]
                    
                    #第一次出現在dic中的ordernumber
                    if ordernum not in orders_dic:
                        data={
                            "ordernum":ordernum,
                            "trip":[],
                            "totalPrice":trip["totalPrice"],
                            "status":trip["status"]
                            }
                        orders_dic[ordernum]=data 
                    trip_list=orders_dic[ordernum]["trip"]
                    trip={
                        "attractionName": trip["attractionName"],
                        "date": datetime.strftime(trip["date"], "%Y-%m-%d"),
                        "time":trip["time"],
                        "price":trip["price"],
                    }
                    trip_list.append(trip)
                    
                for value in orders_dic.values():
                    all_count+=1
                    orders_history_list.append(value)
                    
                    
                #一次只有show最多六筆訂單    
                count=all_count-page*6
                if count<6:
                    nextPage=None
                else:
                    nextPage=page+1                 
                return jsonify({"nextPage": nextPage, "data": orders_history_list[page*6:6+6*page]})
            else:
                return jsonify({"error":True,"message":"未曾有歷史訂單"})       
        else:
            return jsonify({"error":True,"message":"請先登入"})            
    except:
        return jsonify({"error": True, "message": "伺服器內部錯誤"})                       
                
                
                
                
                
                
                
                
                
                
                
                
       
        
                           
    
               
            
        
            
            
            
            

