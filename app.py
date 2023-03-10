import os
import json
import logging
import datetime

import pymongo
from flask_cors import CORS
from flask_socketio import SocketIO
from flask.logging import wsgi_errors_stream
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", engineio_logger=True, async_mode="gevent")

# MongoDB client
mongo_client = pymongo.MongoClient(os.getenv('MONGODB'))


logging.basicConfig(format='%(asctime)s - %(name)s -> %(levelname)s: %(message)s',
                            datefmt="%Y-%m-%d %H:%M:%S",
                            handlers=[
                                logging.StreamHandler(stream=wsgi_errors_stream),
                            ],
                            level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_mongodb_collection():
    db = mongo_client[os.getenv("MONGODB_DATABSE")]
    events_collection = db[os.getenv("MONGODB_DATABSE_COLLECTION")]

    return events_collection


@socketio.on('message', namespace="/events")
def handle_message(data):
    event = data.get("event")
    if event == "connect":
        logger.info(f"\n{50*'='} \n Client connected SID:{request.sid} \n{50*'='}")
    elif event == "disconnect":
        logger.info(f"\n{50*'='} \n Client disconnected SID:{request.sid} \n{50*'='}")


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
        body = body.get("mandrill_events")
        if not body:
            return jsonify({"msg": "Missing mandrill_events in received data"}), 400
        
        body = json.loads(body)
        if len(body) == 0:
            return "", 200

        # Parse received data body
        body = list(map(lambda x: parse_body(x), body))

        try:
            # Insert events to MongoDB
            events_collection = get_mongodb_collection()
            events_collection.insert_many(body) 
        except pymongo.errors.BulkWriteError:
            raise Exception("MongoDB insert failed")
        except pymongo.errors.ConnectionFailure:
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
