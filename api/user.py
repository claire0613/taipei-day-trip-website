
import sys
sys.path.append("..")
from database import search_users,insert_user
from flask import Blueprint, session, request, jsonify,make_response
import time
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()
api_user = Blueprint('api_user', __name__)


@api_user.route('/user',methods=['GET'])
def get_user():
    try:
        # 有登入
        token_cookie=request.cookies.get('user_cookie')
        if token_cookie :
            user=jwt.decode(token_cookie,os.getenv("SECRET_KEY"),algorithms=['HS256'])
            data = {"data":user}
            return jsonify(data)
        #  token 超時 or 未登入
        else:
            data = {"data": None}
            return jsonify(data)

    except:
        return jsonify({"error": True, "message": "伺服器內部錯誤"})

@api_user.route('/user',methods=['POST'])
def signup():
    try:
        data=request.json
        name = data['name']
        email = data['email']
        password = data['password']
        is_user_exist= search_users(email = email)
        if not is_user_exist:
            insert_user(name=name,email=email,password=password)
            
            return jsonify({"ok":True})
        else:
            return jsonify({ "error": True, "message": "註冊失敗，此Email已被註冊" })
    # 伺服器錯誤
    except:
        error = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(error), 500
@api_user.route('/user',methods=['PATCH'])
def signin():
    try:
        data = request.json
        email = data['email']
        password = data['password']
        signin=search_users(email=email,password=password)
        # 登入成功
        if signin:
            token=jwt.encode({
            "id": signin['id'],
            "name": signin['name'],
            "email": signin['email'],"exp": datetime.utcnow() + timedelta(minutes=1)
        },os.getenv("SECRET_KEY"),algorithm='HS256')
            message = {"ok": True}
            response = make_response(jsonify(message))
            response.set_cookie(key='user_cookie', value=token)
            return response
   
        # 登入失敗
        else:
            message = {
            "error": True,
            "message": "登入失敗，帳號或密碼輸入錯誤"
            }
            response = make_response(jsonify(message), 400)
            return response

    # 伺服器錯誤
    except:
        message = {
            "error": True,
            "message": "伺服器內部錯誤"
            }
        response = make_response(jsonify(message), 500)
        return response
    
@api_user.route('/user', methods=['DELETE'])
def singout():
    # 登出
    message = {"ok": True}
    response=make_response(jsonify(message))
    response.set_cookie(key='user_cookie', value='', expires=0)
    return response