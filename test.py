from flask import Flask, request, jsonify, render_template_string
import json
import requests

app = Flask(__name__)

# Fungsi untuk mendapatkan IP klien secara akurat
def get_client_ip():
    headers_to_check = [
        'X-Forwarded-For', 'X-Real-IP', 'CF-Connecting-IP', 'Forwarded', 'True-Client-IP'
    ]
    for header in headers_to_check:
        if request.headers.get(header):
            return request.headers.get(header).split(',')[0].strip()
    return request.remote_addr

# Fungsi untuk mendapatkan asal negara dari IP
def get_country_from_ip(ip):
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/', timeout=5)
        data = response.json()
        return data.get('country_name', 'Unknown')
    except:
        return 'Unknown'

@app.route('/')
def index():
    ip = get_client_ip()
    country = get_country_from_ip(ip)

    # Log semua header untuk debugging
    print("Request Headers:", request.headers)

    # Mencatat data pengunjung
    visitor_data = {"ip": ip, "country": country}
    try:
        with open('data.js', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(visitor_data)
    with open('data.js', 'w') as file:
        json.dump(data, file, indent=4)

    return render_template_string('<h1>Welcome</h1>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
