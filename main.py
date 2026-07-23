# app.py
from flask import Flask, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import socket

app = Flask(__name__)

REQUEST_COUNT = Counter('flask_request_count', 'Total number of requests', ['endpoint'])

@app.route('/')
def print_ip():
    REQUEST_COUNT.labels(endpoint='home').inc()
    return "This is my application home page"

@app.route('/login')
def login_page():
    REQUEST_COUNT.labels(endpoint='login').inc()
    return "This is login page."

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
