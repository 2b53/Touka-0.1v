# Installiere gunicorn mit pip install gunicorn
subprocess.Popen(["gunicorn", "Bot:app", "-b", "0.0.0.0:5001"])
