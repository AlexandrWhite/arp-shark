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


def get_data(mac_address, period_name, period_value):
    query = f'SELECT event_time, INET_NTOA(switch_ip) as switch_ip, mac_addr, \
        port_name, oper_id, vlan_id FROM event where mac_addr=\'{mac_address}\''
    if period_name == 'days':
        query += f'and event_time >= NOW() - INTERVAL {period_value} DAY'
    if period_name == 'months':
        query += f'and event_time >= NOW() - INTERVAL {period_value} MONTH'
    if period_name == 'hours':
        query += f'and event_time >= NOW() - INTERVAL {period_value} HOUR'
    query = text(query)
    result = db.session.execute(query)
    return result


def solve_open_conflicts(data):
    pass 
def clear_data(data):
    data = solve_open_conflicts(data)


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
    period_value = request.form['period-unit']
    period_name = request.form['period-names']

    result = get_data(mac_address,period_name,period_value)
    intervals = get_intervals(mac_address)
    return render_template('test.html', events=result,intervals = intervals)


@app.route('/')
def hello_world():
    return render_template('test.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)