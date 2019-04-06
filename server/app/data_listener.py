from app import mqtt
from .data_handler import DataHandler
from .db_handler import DatabaseHandler
from flask import Blueprint, Response
import time
import redis
import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

# The location to receive data from
PHYSICAL_AREA = config.get("DEFAULT", "PHYSICAL_AREA")

REDIS_SERVER = config.get("DEFAULT", "REDIS_SERVER")
REDIS_PORT = config.getint("DEFAULT", "REDIS_PORT")

events_api = Blueprint("events_api", __name__)

red = redis.StrictRedis(host=REDIS_SERVER, port=REDIS_PORT,
                        decode_responses=True)

# red_pubsub = red.pubsub(ignore_subscribe_messages=True)
# red_pubsub.subscribe("events")

data_handler = DataHandler()
db_handler = DatabaseHandler()


@mqtt.on_connect()
def mqtt_on_connect(client, userdata, flags, rc):
    """Event handler for MQTT connection"""
    print("Connected to the broker with status code " + str(rc))
    mqtt.subscribe(PHYSICAL_AREA + "/+")


@mqtt.on_message()
def mqtt_on_message(client, userdata, msg):
    """Event handler for MQTT message"""
    json_data = msg.payload.decode("utf-8")
    data = data_handler.from_json(json_data)

    # Publish the data to the Redis db
    red.publish("events", json_data)

    devices_count = data["devices_count"]
    devices_found = data_handler.is_device_found(devices_count)

    # Only save to db if devices found
    if devices_found:
        db_handler.add(data)


# def send_event():
#     print("sub to redis")

#     msg = red_pubsub.get_message()
#     if msg:
#         print(msg)
#         yield str(msg)
#         time.sleep(0.001)  # Let's be nice to the system


# @events_api.route("/data/events")
# def event():
#     return Response(
#         send_event(),
#         mimetype="text/event-stream"
#     )


def send_event():
    pubsub = red.pubsub()
    pubsub.subscribe("events")
    for msg in pubsub.listen():
        print(msg)
        yield "data: %s\n\n" % msg["data"]


@events_api.route("/data/events")
def sse():
    """Sends the data to client as Server-sent event"""
    return Response(
        send_event(),
        mimetype="text/event-stream")
