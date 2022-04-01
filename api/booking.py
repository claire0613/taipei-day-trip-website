from flask import Blueprint, session, request, jsonify
import sys
import json
from datetime import datetime, date
import jwt
import os
from database import remove_booking, search_booking,insert_booking
sys.path.append("..")

api_booking=Blueprint('api_booking',__name__)


@api_booking.route('/booking',methods=['GET'])
def get_booking():
    try:
        token_cookie=request.cookies.get('user_cookie')
        if token_cookie:
            user=jwt.decode(token_cookie,os.getenv("SECRET_KEY"),algorithms=['HS256'])
            user_id=int(user["id"])
            searchingbooking=search_booking(user_id=user_id)
            print(searchingbooking)
            if searchingbooking:
                data = {
               "attraction": {
                  "id": searchingbooking["id"],
                  "name": searchingbooking["name"],
                  "address": searchingbooking["address"],
                  "image": searchingbooking["image"]
               },
               "date": datetime.strftime( searchingbooking["date"], "%Y-%m-%d"),
               "time": searchingbooking["time"],
               "price":  searchingbooking["price"],
            }
                return jsonify({ "data": data })
            else:
                return jsonify({ "message": "目前沒有行程"})
        else:
            return jsonify({"error":True,"message":"請先登入"})
            
    except:
        return jsonify({"error": True, "message": "伺服器內部錯誤"})
@api_booking.route('/booking', methods=["POST"])
def post_booking():
    try:
        token_cookie=request.cookies.get('user_cookie')
        if token_cookie:
            user=jwt.decode(token_cookie,os.getenv("SECRET_KEY"),algorithms=['HS256'])
            user_id = int(user["id"])
            booking=request.json
            attraction_id = booking["attractionId"]
            date = booking["date"]
            time = booking["time"]
            price = booking["price"]
            if attraction_id and date and time and price and user_id:
                    # 建立行程
                    insert_booking(user_id=user_id, attraction_id=attraction_id, date=date, time=time, price=price)
                    data = {"ok": True}
                    return jsonify(data)
            else:
                # 輸入內容有誤
                data = {
                    "error": True,
                    "message": "行程建立失敗，輸入不正確或其他原因"
                }
                return jsonify(data), 400
        # 沒有登入
        data = {
            "error": True,
            "message": "未登入系統，行程建立失敗"
        }
        return jsonify(data), 403
    # 伺服器（資料庫）連線失敗
    except:
        data = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(data), 500
    
@api_booking.route("/booking", methods=["DELETE"])
def deleteBooking():
   try:
        token_cookie=request.cookies.get('user_cookie')
        if token_cookie:
            user=jwt.decode(token_cookie,os.getenv("SECRET_KEY"),algorithms=['HS256'])
            user_id = int(user["id"])
            remove=remove_booking(user_id = user_id)
            if remove:
                return jsonify({ "ok": True })
            else:
                return jsonify({ "error": True, "message": "刪除失敗" })
        else:
            return jsonify({ "error": True, "message": "未登入系統，拒絕存取" })
   except:
      return jsonify({ "error": True, "message": "伺服器內部錯誤" })