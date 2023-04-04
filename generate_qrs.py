import pyqrcode
import random
import hashlib
from datetime import datetime
from json import load
import pandas as pd
from tqdm import tqdm
import os

# if QRs folder doesn't exist, create it
if os.path.exists("QRs") is False:
    os.mkdir("QRs")
# if stats.json doesn't exist, create it
if os.path.exists("stats.json") is False:
    with open("stats.json", "w") as f:
        f.write("")

with open("local_settings.json") as f:
    local_settings = load(f)
    IP = local_settings["IP"]
    PORT = local_settings["PORT"]
    people = local_settings["people"]
    DOMAIN = f"http://{IP}:{PORT}"

URL = f"{DOMAIN}/verify/"

scale = 8  # Size of QR code:
# higher scale value means more resolution, but bigger file size
# with scale = 8, the size of the file comes to be around 575 bytes

def get_random_string(email):
    salt = str(random.random()) + str(datetime.now())  # A random string
    m = hashlib.sha3_256((salt + email).encode('utf-8')).hexdigest()
    return m[:10] + m[-10:]

def create_qr(email, scale=scale):
    s = get_random_string(email)
    url = pyqrcode.create(URL + s)
    loc = f'QRs/{s}.png'
    url.png(loc, scale = scale)
    return loc

data = pd.read_csv(people).to_dict(orient="records")

for person in tqdm(data):
    create_qr(person["email"])