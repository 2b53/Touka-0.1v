from flask import Flask
from threading import Thread
import time  # Füge das time-Modul hinzu

app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()
    time.sleep(5)  # Wartezeit in Sekunden (kann angepasst werden)
    server.join()  # Warten, bis der Thread beendet ist