from json import load, dump
from flask import Flask

with open("local_settings.json") as f:
    local_settings = load(f)
    IP = local_settings["IP"]
    PORT = local_settings["PORT"]

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/verify/<string:code>')
def verify(code):
    with open("stats.json") as f:
        stats = load(f)
    
    if code not in stats:
        return "Invalid QR"
    
    if stats[code]["count"]:
        stats[code]["count"] -= 1
        with open("stats.json", "w") as f: dump(stats, f)
        return f"Valid QR: {stats[code]['count']} scans left"
    
    return "QR Expired"

app.run(host=IP, port=PORT, debug=True)