import sys
sys.path.append("..")
from database import search_attracion,search_attractionid
from flask import *


api = Blueprint('api', __name__)

@api.route('/attractions', methods=['GET'])
def get_attraction():
    try: 
      
        page = int(request.args.get('page'))
        keyword=request.args.get('keyword')
        if page <0 :
            return jsonify({"error": True, "message": "page < 0"})
        data = search_attracion(page=page,keyword=keyword)
        return jsonify({"nextPage": page+1, "data": data})


    except:
            return jsonify({"error": True, "message": "伺服器內部錯誤"})
@api.route('/attraction/<attractionId>', methods=['GET'])
def get_attractionid(attractionId):
    try:
        if attractionId:
            data=search_attractionid(attractionId)
            return jsonify({"data": data})
        else:
            return jsonify({"error": True, "message": "景點編號不正確"})
        
    except:
        return jsonify({"error": True, "message": "伺服器內部錯誤"})
