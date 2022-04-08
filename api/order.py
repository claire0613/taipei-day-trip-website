from tkinter.tix import Tree
from turtle import update
from flask import Blueprint, session, request, jsonify

import requests
import sys
import json
from datetime import datetime, date
import jwt
import os
from database import search_booking, search_ordernum, update_booking_for_order, update_booking_for_pay
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
            user_id=int(user["id"])
            order=request.json 
            prime=order['prime']
            total_price=int(order['order']['price'])
            name=order['order']['contact']['name']
            email=order['order']['contact']['email']
            phone=order['order']['contact']['phone']
            order_num=datetime.now().strftime('%Y%m%d%H%M%S%f')
            
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
                        return jsonify(tappay)
                    else:
                        tappay={
                            "error":True,
                            "message": "付款狀態更改失敗"
                            }
                    return jsonify(tappay)
                else:
                    tappay={
                            "error":True,
                            "message": "付款失敗"
                            }
                    return jsonify(tappay)
                
        else:
            return jsonify({"error":True,"message":"請先登入"})       
    except:
        return jsonify({"error": True, "message": "伺服器內部錯誤"})     
            
               
            
        
            
            
            
            
# @api_orders.route('/orders',methods=['POST'])
       