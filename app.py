import os
import json
import logging
import datetime

import pymongo
from flask_cors import CORS
from flask_socketio import SocketIO
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "aN0t4wZwOwdhe08AVk6wTYZkmTt4YlSK")
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", engineio_logger=True, async_mode="gevent")

# MongoDB client
mongo_uri = os.getenv('MONGODB', "mongodb://root:rootpassword@127.0.0.1:27017")
mongo_client = pymongo.MongoClient(mongo_uri)
db = mongo_client.db
events_collection = db.events


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@socketio.on('message', namespace="/events")
def handle_message(data):
    event = data.get("event")
    if event == "connect":
        logger.info(f"Client connected SID:{request.sid}")
    elif event == "disconnect":
        logger.info(f"Client disconnected SID:{request.sid}")


@app.route("/event", methods=["POST"])
def get_events():
    def parse_body(event):
        """
        Parse event json got from webhook call
        and rename `_id` key to 'id' because of 
        confliction with monogodb default key `_id`
        :param: event: event json received from mandrill 
        """
        event["id"] = event.pop("_id", None)
        return event
    
    try:
        body = request.form.to_dict()
        body = body["mandrill_events"]
        body = json.loads(body)

        # Parse received data body
        body = list(map(lambda x: parse_body(x), body))

        try:
            # Insert events to MongoDB
            events_collection.insert_many(body) 
        except pymongo.errors.BulkWriteError:
            raise Exception("MongoDB insert failed")
        except pymongo.errors.ConnectionFailure as ex:
            raise Exception("MongoDB connection error")

        ret = []
        for event in list(body):
            ret.append({
                "event": event.get("event", "Event"),
                "ts": datetime.datetime.fromtimestamp(event["ts"]).strftime("%Y/%m/%d %H:%M:%S")
            })

        socketio.send(ret, namespace="/events")

        return "", 200
    except Exception:
        logger.exception("@get_events")
        return jsonify({"msg": "Internal Error!"}), 500


@app.route('/')
def main_page():
    return render_template("index.html")


if __name__ == '__main__':
    socketio.run(app)
