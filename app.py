import os
import json
import logging
import datetime

import pymongo
from flask_cors import CORS
from flask_socketio import SocketIO
from pymongo.collection import Collection
from flask.logging import wsgi_errors_stream
from flask import Flask, render_template, request, jsonify, Response


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


class DbInsertEventError(Exception):
    pass


class DbConnectionError(Exception):
    pass


def get_mongodb_collection() -> Collection:
    db = mongo_client[os.getenv("MONGODB_DATABSE")]
    events_collection = db[os.getenv("MONGODB_DATABSE_COLLECTION")]

    return events_collection


@socketio.on('message', namespace="/events")
def handle_message(data: json) -> None:
    event = data.get("event")
    if event == "connect":
        logger.info(f"\n{50*'='} \n Client connected SID:{request.sid} \n{50*'='}")
    elif event == "disconnect":
        logger.info(f"\n{50*'='} \n Client disconnected SID:{request.sid} \n{50*'='}")


def parse_body(event: json) -> json:
        """
        Parse event json got from webhook call
        and rename `_id` key to 'id' because of 
        confliction with monogodb default key `_id`
        :param: event: event json received from mandrill 
        """
        event["id"] = event.pop("_id", None)
        return event


@app.route("/event", methods=["POST"])
def get_events() -> Response:
    try:
        body = request.form.to_dict()
        body = body.get("mandrill_events")
        if not body:
            return jsonify({"msg": "Missing mandrill_events in received data"}), 400
        
        body = json.loads(body)
        if len(body) == 0:
            return "", 200

        # Parse received data body
        body = list(map(parse_body, body))

        try:
            # Insert events to MongoDB
            events_collection = get_mongodb_collection()
            events_collection.insert_many(body) 
        except pymongo.errors.BulkWriteError:
            raise DbInsertEventError("Database insert failed")
        except pymongo.errors.ConnectionFailure:
            raise DbConnectionError("Database connection error")

        ret = []
        for event in list(body):
            ret.append({
                "event": event.get("event", "Event"),
                "ts": datetime.datetime.fromtimestamp(event["ts"]).strftime("%Y/%m/%d %H:%M:%S")
            })

        socketio.send(ret, namespace="/events")

        return "", 200
    except (DbInsertEventError, DbConnectionError) as ex:
        logger.exception("@get_events")
        return jsonify({"msg": str(ex)}), 500
    except Exception:
        logger.exception("@get_events")
        return jsonify({"msg": "Internal Error!"}), 500


@app.route('/')
def main_page() -> Response:
    return render_template("index.html")


if __name__ == '__main__':
    socketio.run(app)
