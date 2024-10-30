from flask import Flask,render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask import request
import os
from dotenv import load_dotenv
import json 

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("MYSQL_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



@app.route('/mac_history', methods=['POST'])
def mac_history():
    print(request)
    data = request.get_json()
    mac_address = data.get('mac-address')

    query = f"SELECT event_time, INET_NTOA(switch_ip) as switch_ip, mac_addr FROM event where mac_addr='{mac_address}'"
    query = text(query)
    result = db.session.execute(query)
    json_result = json.dumps([ row._asdict() for row in result ], sort_keys=True, default=str)

    return jsonify(json_result),200




@app.route('/')
def hello_world():
    return render_template('test.html')



if __name__ == '__main__':
    app.run(debug=True)