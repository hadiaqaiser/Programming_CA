# start small flask app for medoracare project, only add simple /api/ping

from flask import Flask, jsonify
from flask_cors import CORS

# import my shared db things (engine + Base) and models so tables can be created once
from backend.db import engine, Base
from backend import models  # just import so models register with Base

# create main flask application
app = Flask(__name__)

# small endpoint to test if backend alive
@app.get("/api/ping")
def ping():
    return jsonify({"message": "medoracare api ok"})


# this only runs if i do: python app.py (optional)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
