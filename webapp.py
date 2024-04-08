from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    try:
        with open('backup.json', 'r') as file:
            backup_data = json.load(file)
            return render_template('index.html', backup_data=backup_data)
    except FileNotFoundError:
        return 'No backup found. Create a backup using !backup.'

if __name__ == '__main__':
    app.run(debug=True)
