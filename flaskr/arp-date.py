from flask import Flask,render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask import request
import os 


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("MYSQL_SECRET")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



@app.route('/', methods=['POST','GET'])
def execute_query():
   
    target_mac = ''
    if request.method == 'POST':
        target_mac = request.form['mac-address']

    query = f"SELECT event_time, INET_NTOA(switch_ip) as switch_ip, mac_addr FROM event where mac_addr='{target_mac}'"

    query = text(query)
    result = db.session.execute(query)
    return render_template('test.html', events=result)

@app.route('/')
def hello_world():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)