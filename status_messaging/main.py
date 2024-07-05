from datetime import datetime
import threading
import sys
import json
import time

from uvicorn import run
from fastapi import FastAPI, File, HTTPException, UploadFile, Form
from mqtt_server import mqtt_client, start_mqtt
from config import configs
from mongoDB_connection import mycol
from random import randrange


app = FastAPI()


def publish_continuously():
    while True:
        results = {"status": randrange(0, 6)}

        print('Publish to MQTT {}'.format(configs['topic']), flush=True)
        rc, mid = mqtt_client.publish(configs['topic'], json.dumps(results), qos=2)
        print(f"Code {rc} while sending message {mid}")
        if rc == 0:
            results.update({
                "updated_on": datetime.now().strftime(configs["datetime_format"])
            })
            x = mycol.insert_one(results)
            print(f"inserted {x.inserted_id} into MONGODB on {results['updated_on']}")
        time.sleep(1)


@app.on_event("startup")
async def startup_event():
    start_mqtt()
    print("Starting continuous publishing thread...")
    threading.Thread(target=publish_continuously, daemon=True).start()


@app.get("/delete_records")
async def delete():
    d = mycol.delete_many({})
    return {"status": f"{d.deleted_count} records deleted"}


@app.get("/")
async def main(start_time: str = None, end_time: str = None):
    """
    required query string hosturl/?start_time=12:57:37&end_time=12:57:52
    time string should be 24H format
    :param start_time:
    :param end_time:
    :return:
    """
    if not start_time and not end_time:
        start_time = "12:57:37"
        end_time = "12:57:52"
    try:
        for x in mycol.find():
            print({
                "status": x.get("status"),
                "time": x.get("updated_on")
            })
        required_status = mycol.count_documents({"updated_on": {"$gt": start_time, "$lt": end_time}})
        print(f"result for {start_time} to {end_time} is {required_status}")
        return f"result is {required_status}"
    except:
        e = sys.exc_info()
        print('Python error with no Exception handler:')
        print('Traceback error: {} on {}'.format(e[1], e[2].tb_lineno))
        raise HTTPException(status_code=500, detail=str(e[1]))


if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8000)
