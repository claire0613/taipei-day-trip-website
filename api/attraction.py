import sys
sys.path.append("..")
from database import search_attracion,search_attractionid,attraction_count
from flask import *
api = Blueprint('api', __name__)

@api.route('/attractions', methods=['GET'])
def get_attraction():
    try: 
      
        page = int(request.args.get('page'))
        keyword=request.args.get('keyword')
        allcount=attraction_count(page=page,keyword=keyword)
        data = search_attracion(page=page,keyword=keyword)
        count=allcount-page*12
        if count<12:
            nextpage=None
        else:
            nextpage=page+1
        return jsonify({"nextPage": nextpage, "data": data}) 
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
