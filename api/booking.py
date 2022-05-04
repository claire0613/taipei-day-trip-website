from flask import Blueprint, session, request, jsonify
import sys
import json
from datetime import datetime, date
import jwt
import os
from dotenv import load_dotenv
load_dotenv()
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
            bookings=search_booking(user_id=user_id)
            if bookings:
                booking_list=[]
                for booking in bookings:
                    data = {
                    "bookingId":booking["bookingId"],
                "attraction": {
                    "id": booking["attractionId"],
                    "name": booking["name"],
                    "address": booking["address"],
                    "image": booking["image"]
                },
                "date": datetime.strftime(booking["date"], "%Y-%m-%d"),
                "time": booking["time"],
                "price": booking["price"],
                    }
                    booking_list.append(data)  
                return jsonify({ "data": booking_list })
            else:
                return jsonify({ "data": None,"message":"目前無預定行程" })

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
            if attraction_id and date and (time == 'morning' and price == 2000) or (time == 'afternoon' and price == 2500)and user_id:
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
            booking=request.json
            booking_id=booking["bookingId"]
            remove=remove_booking(booking_id = booking_id)
            if remove:
                return jsonify({ "ok": True })
            else:
                return jsonify({ "error": True, "message": "刪除失敗" })
        else:
            return jsonify({ "error": True, "message": "未登入系統，拒絕存取" })
   except:
      return jsonify({ "error": True, "message": "伺服器內部錯誤" })