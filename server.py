import os
if not os.path.exists("stats.json"):
    raise FileNotFoundError("'stats.json' not found, follow the steps in README.md")

from json import load, dump
from flask import Flask, render_template

with open("local_settings.json") as f:
    local_settings = load(f)
    IP = local_settings["IP"]
    PORT = local_settings["PORT"]

app = Flask(__name__)

@app.route('/')
def hello_world():
    with open("stats.json") as f:
        stats = load(f).values()
    left = sum([int(i["count"]) for i in stats])
    return render_template("log.html", items = stats, left = left)

@app.route('/verify/<string:code>')
def verify(code):
    with open("stats.json") as f:
        stats = load(f)

    if code not in stats:
        return "<h1>Invalid QR</h1>"

    if int(stats[code]["count"]):
        stats[code]["count"] = int(stats[code]["count"])-1
        with open("stats.json", "w") as f: dump(stats, f)
        return f"<h1>Valid QR: {stats[code]['count']} scans left</h1>"
    
    return "<h1>QR Expired</h1>"

app.run(host=IP, port=PORT, debug=False)