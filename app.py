import os
import time
import threading
import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

current_status = {
    "status": "checking",
    "latency": 0,
    "code": "--",
    "last_updated": ""
}
TARGETS = {
    "google": "https://www.google.com",
    "github": "https://github.com",
}
current_statuses = {}

def monitor_all_targets():
    global current_statuses
    
    for name in TARGETS:
        current_statuses[name] = {"status": "checking", "latency": 0, "code": "--"}

    while True:
        for name, url in TARGETS.items():
            try:
                response = requests.head(url, timeout=3)
                latency = round(response.elapsed.total_seconds() * 1000)
                
                if response.status_code == 200:
                    status = "ok" if latency < 500 else "slow"
                else:
                    status = "down"
                
                current_statuses[name] = {
                    "status": status,
                    "latency": latency,
                    "code": response.status_code
                }
            except Exception:
                current_statuses[name] = {
                    "status": "down",
                    "latency": 0,
                    "code": "Error"
                }
        
        time.sleep(10)

@app.route('/')
def monitor():
    return render_template('index.html', title='サーバー監視')

@app.route('/getinfo')
def getinfo():
    return jsonify(current_statuses)

if __name__ == '__main__':
    threading.Thread(target=monitor_all_targets, daemon=True).start()
    app.run(use_reloader=False)
