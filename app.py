from api.attraction import api
from api.user import api_user
from api.booking import api_booking
from flask import *
import jwt
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
# register blueprint
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(api_user, url_prefix='/api')
app.register_blueprint(api_booking, url_prefix='/api')
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["JSON_SORT_KEYS"]=False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")






# Pages

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000)
