

from database import search_users, insert_user, updated_name_pwd
from flask import Blueprint, session, request, jsonify, make_response
from database import updated_name_pwd
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import jwt,re,sys
import time
from werkzeug.security import generate_password_hash,check_password_hash
from models.usermodel import User
sys.path.append("..")
load_dotenv()
api_user = Blueprint('api_user', __name__)


@api_user.route('/user', methods=['GET'])
def get_user():
    try:
        # 有登入
        token_cookie = request.cookies.get('user_cookie')
        if token_cookie:
            user = jwt.decode(token_cookie, os.getenv(
                "SECRET_KEY"), algorithms=['HS256'])
            data = {"data": user}
            return jsonify(data)
        #  token 超時 or 未登入
        else:
            data = {"data": None}
            return jsonify(data)

    except:
        return jsonify({"error": True, "message": "伺服器內部錯誤"})


@api_user.route('/user', methods=['POST'])
def signup():
    try:
        data = request.json
        # name = data['name']
        # email = data['email']
        # password = data['password']
        is_user_exist = search_users(email=data['email'])
        input_data=User(name=data['name'],email=data['email'],password=data['password'])
        if not is_user_exist:
            if  len(input_data.name)>2 and len(data['password'])>2 and \
                bool(re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',input_data.email)):
                insert = insert_user(name=input_data.name, email=input_data.email, password=input_data._password_hash)
                if insert:
                    return jsonify({"ok": True})
                return jsonify({"error": True, "message": "資料庫註冊失敗"})
            else:
                return jsonify({"error": True, "message": "帳號、密碼或信箱格式有誤"})
        else:
            return jsonify({"error": True, "message": "註冊失敗，此Email已被註冊"})
    # 伺服器錯誤
    except:
        error = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(error), 500


@api_user.route('/user', methods=['PATCH'])
def signin():
    try:
        data = request.json
        email = data['email']
        password = data['password']
        signin = search_users(email=email)
        passed=check_password_hash(signin['password'],password)
        # 登入成功
        if passed:
            token = jwt.encode({
                "id": signin['id'],
                "name": signin['name'],
                "email": signin['email'], "exp": datetime.utcnow() + timedelta(days=1)
            }, os.getenv("SECRET_KEY"), algorithm='HS256')
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
    response = make_response(jsonify(message))
    response.set_cookie(key='user_cookie', value='', expires=0)
    return response


# 修改會員姓名/密碼
@api_user.route('/member', methods=['POST'])
def updateuser():
    try:
        token_cookie=request.cookies.get('user_cookie')
        if token_cookie :
            user=jwt.decode(token_cookie,os.getenv("SECRET_KEY"),algorithms=['HS256'])
            user_id=user["id"]
            data = request.json
            newname = data["newName"]
            pwd=data["pwd"]
            result=updated_name_pwd(user_id=user_id, new_name=newname,pwd=pwd)
            if result:
                message = {"ok": True}
                response = make_response(jsonify(message))
                if newname:
                    token = jwt.encode({
                    "id": user['id'],
                    "name": newname,
                    "email": user['email'], "exp": datetime.utcnow() + timedelta(days=1)
                    }, os.getenv("SECRET_KEY"), algorithm='HS256')
                    response.set_cookie(key='user_cookie', value=token)
                    return response
                else:
                    return response
            
        else:
            return jsonify({"error": True,"message":"未登入"})
    # 伺服器錯誤
    except:
        message = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        response = make_response(jsonify(message), 500)
        return response

