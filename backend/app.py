# start small flask app for medoracare project, only add simple /api/ping

from flask import Flask, jsonify

# create main flask application
app = Flask(__name__)

# small endpoint to test if backend alive
@app.get("/api/ping")
def ping():
    return jsonify({"message": "medoracare api ok"})


# this only runs if i do: python app.py (optional)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)