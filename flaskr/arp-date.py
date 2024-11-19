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


def get_data(mac_address):
    query = f"SELECT event_time, INET_NTOA(switch_ip) as switch_ip, mac_addr, oper_id FROM event where mac_addr='{mac_address}'"
    query = text(query)
    result = db.session.execute(query)
    return result

def get_intervals(mac_address):
    query = f"""
        SELECT sub2.time_op1 as start, sub2.time_op2 as finish  FROM 
    (SELECT  
        t1.event_time as time_op1,
        t2.event_time as time_op2
    FROM
        (SELECT  event_time,mac_addr,oper_id 
            from mac_notif.event WHERE mac_addr ='{mac_address}') t1
    JOIN  (SELECT  event_time,mac_addr,oper_id 
            from mac_notif.event WHERE mac_addr ='{mac_address}') t2
    ON t2.oper_id =2 AND t2.event_time  > t1.event_time 
    WHERE  
        t1.oper_id = 1) sub2
    GROUP BY 
        start
    """
    query = text(query)
    result = db.session.execute(query)
    return result



@app.route('/mac_json', methods=['POST'])
def mac_history():
    data = request.get_json()
    mac_address = data.get('mac-address')
    result = get_data(mac_address)
    json_result = json.dumps([ row._asdict() for row in result ], sort_keys=True, default=str)
    return jsonify(json_result),200

@app.route('/mac_table', methods=['POST'])
def mac_table():
    mac_address = request.form['mac-address']
    result = get_data(mac_address)
    intervals = get_intervals(mac_address)
    return render_template('test.html', events=result,intervals = intervals)


@app.route('/')
def hello_world():
    return render_template('test.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)