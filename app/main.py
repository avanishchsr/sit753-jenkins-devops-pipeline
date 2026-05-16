from flask import Flask, jsonify
import os
import time

app = Flask(__name__)
START_TIME = time.time()

@app.route('/')
def home():
    return jsonify({
        'application': 'Student Connect API',
        'status': 'running',
        'environment': os.getenv('APP_ENV', 'development'),
        'message': 'A small deployable Flask service used to demonstrate a Jenkins DevOps pipeline.'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'uptime_seconds': round(time.time() - START_TIME, 2)})

@app.route('/api/jobs')
def jobs():
    return jsonify([
        {'id': 1, 'title': 'Retail Assistant', 'type': 'Part-time', 'location': 'Melbourne'},
        {'id': 2, 'title': 'Cafe Staff', 'type': 'Casual', 'location': 'Melbourne'},
        {'id': 3, 'title': 'Data Internship', 'type': 'Internship', 'location': 'Hybrid'}
    ])

@app.route('/api/groups')
def groups():
    return jsonify([
        {'id': 1, 'name': 'Indian Students Melbourne', 'category': 'Community'},
        {'id': 2, 'name': 'Deakin Tech Community', 'category': 'Technology'}
    ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
