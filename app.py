from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from user_agents import parse
import hashlib
import json
import requests
from datetime import timedelta

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///analytics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class PageVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_hash = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    exit_time = db.Column(db.DateTime, nullable=True)
    device_type = db.Column(db.String(50))
    browser = db.Column(db.String(50))
    os = db.Column(db.String(50))
    country = db.Column(db.String(50))
    city = db.Column(db.String(50))
    url_path = db.Column(db.String(500))
    referrer = db.Column(db.String(500))
    screen_resolution = db.Column(db.String(20))
    session_duration = db.Column(db.Integer, nullable=True)  # in seconds

def get_location_data(ip):
    # For localhost testing, return actual location
    if ip == '127.0.0.1':
        return {
            'country': 'Russia',  # Change to your actual country
            'city': 'Moscow'      # Change to your actual city
        }
    
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
        if data['status'] == 'success':
            return {
                'country': data['country'],
                'city': data['city']
            }
    except:
        pass
    return {'country': 'Unknown', 'city': 'Unknown'}

@app.route('/analytics/collect', methods=['POST'])
def collect_data():
    try:
        data = request.get_json()
        user_agent = parse(request.headers.get('User-Agent', ''))
        
        # Get IP and location data
        ip = request.remote_addr
        location = get_location_data(ip)
        
        session_data = f"{ip}{request.headers.get('User-Agent')}"
        session_hash = hashlib.sha256(session_data.encode()).hexdigest()

        # Handle exit or update events
        if data.get('eventType') in ['exit', 'update']:
            visit = PageVisit.query.filter_by(session_hash=session_hash).order_by(PageVisit.timestamp.desc()).first()
            if visit:
                if data.get('eventType') == 'exit':
                    visit.exit_time = datetime.utcnow()
                visit.session_duration = data.get('duration', 0)
                db.session.commit()
                return jsonify({'status': 'success'}), 200

        visit = PageVisit(
            session_hash=session_hash,
            device_type=user_agent.device.family,
            browser=user_agent.browser.family,
            os=user_agent.os.family,
            country=location['country'],
            city=location['city'],
            url_path=data.get('path', ''),
            referrer=data.get('referrer', ''),
            screen_resolution=data.get('screenResolution', '')
        )
        
        db.session.add(visit)
        db.session.commit()
        
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/')
def demo_page():
    return render_template('analytics_demo.html')

@app.route('/dashboard')
def dashboard():
    visits = PageVisit.query.order_by(PageVisit.timestamp.desc()).limit(10).all()
    data = []
    for visit in visits:
        data.append({
            'timestamp': visit.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'browser': visit.browser,
            'os': visit.os,
            'device_type': visit.device_type,
            'screen_resolution': visit.screen_resolution,
            'url_path': visit.url_path,
            'country': visit.country,
            'city': visit.city,
            'referrer': visit.referrer,
            'session_duration': visit.session_duration or 0
        })
    return render_template('dashboard.html', visits=data)

with app.app_context():
    db.drop_all()  # Add this line to drop existing tables
    db.create_all()  # This will create new tables with updated schema

if __name__ == '__main__':
    app.run(debug=True)