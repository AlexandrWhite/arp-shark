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
        port_name, oper_id, vlan_id, port_id FROM event where mac_addr=\'{mac_address}\''
    if period_name == 'days':
        query += f'and event_time >= NOW() - INTERVAL {period_value} DAY'
    if period_name == 'months':
        query += f'and event_time >= NOW() - INTERVAL {period_value} MONTH'
    if period_name == 'hours':
        query += f'and event_time >= NOW() - INTERVAL {period_value} HOUR'
    query = text(query)
    result = db.session.execute(query)
    return result





from datetime import datetime 
def solve_open_conflicts(data):
    #У меня не получилось нормально работать с типом CursorResult
    d = []
    for row in data:
        date = datetime.fromisoformat(str(row[0]))
        d.append({
            'event_time':date.strftime('%d-%m-%Y  %H:%M:%S'),
            'switch_ip':row[1],
            'mac_addr':row[2],
            'port_name':row[3],
            'oper_id':row[4],
            'vlan_id':row[5],
            'port_id':row[6]            
        })
    return d







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
    result = solve_open_conflicts(result)

    #intervals = get_intervals(mac_address)
    return render_template('test.html', events=result)


@app.route('/')
def hello_world():
    return render_template('test.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)