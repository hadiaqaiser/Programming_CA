# main flask api file for medoracare. here i wire cors, db and all endpoints
# ref: https://flask.palletsprojects.com/en/3.0.x/quickstart/

from flask import Flask, jsonify, request
from flask_cors import CORS

# import my shared db things (engine + Base) and models so tables can be created once
from .db import engine, Base
from . import models

# creating all tables in medora.db if not exist yet (products, shades, batches, wishlist_items, reviews)
# ref: Base.metadata.create_all usage from SQLAlchemy docs https://docs.sqlalchemy.org/en/20/core/metadata.html#create-all-database-objects and chatgpt
Base.metadata.create_all(bind=engine)

# create main flask application
app = Flask(__name__)
CORS(app)

# small endpoint to test if backend alive


@app.get("/api/ping")
def ping():
    return jsonify({"message": "medoracare api ok"})


# this only runs if i do: python app.py (optional)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
