from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import socket
import pymongo
import os
load_dotenv()
global database_url
global database
global collection
global port_p
database_url = os.environ.get('DATABASE_URL')
database = os.environ.get('DATABASE')
collection = os.environ.get('COLLECTION')
port_p = int(os.environ.get('PORT', 5000))
app = Flask(__name__)

mongodb = pymongo.MongoClient(database_url)
db = mongodb[database]
tasks_collection = db[collection]

@app.route("/")
def index():
    hostname = socket.gethostname()
    return jsonify(
        message="Welcome to Tasks app! I am running inside {} pod!".format(hostname)
    )


@app.route("/tasks")
def get_all_tasks():
    tasks = tasks_collection.find()
    data = []
    for task in tasks:
        item = {
            "id": str(task["_id"]),
            "task": task["task"]
        }
        data.append(item)
    return jsonify(
        data=data
    )


@app.route("/task", methods=["POST"])
def create_task():
    data = request.get_json(force=True)
    tasks_collection.insert_one({"task": data["task"]})
    return jsonify(
        message="Task saved successfully!"
    )


@app.route("/task/<id>", methods=["PUT"])
def update_task(id):
    data = request.get_json(force=True)["task"]
    response = tasks_collection.update_one({"_id": ObjectId(id)}, {"$set": {"task": data}})
    if response.matched_count:
        message = "Task updated successfully!"
    else:
        message = "No Task found!"
    return jsonify(
        message=message
    )


@app.route("/task/<id>", methods=["DELETE"])
def delete_task(id):
    response = tasks_collection.delete_one({"_id": ObjectId(id)})
    if response.deleted_count:
        message = "Task deleted successfully!"
    else:
        message = "No Task found!"
    return jsonify(
        message=message
    )


@app.route("/tasks/delete", methods=["POST"])
def delete_all_tasks():
    tasks_collection.delete_many({})
    return jsonify(
        message="All Tasks deleted!"
    )


if __name__ == "__main__":


    app.run(host="0.0.0.0", port=port_p)
