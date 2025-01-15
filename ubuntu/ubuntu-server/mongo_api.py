from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from prettytable import PrettyTable
import json

mongo_uri = "mongodb://hepl:heplhepl@localhost:27017/"
database_name = "reservationDB"
collection_name = "log"

# EXAMPLE: message = 
# {             
#     "topic": "smartoffice/2/1000000044888d31/rfid",
#     "date_log": "2024-12-25T09:15:00Z",
#     "value_log": "0000AEC6680",
#     "id_premise": "1",
#     "id_device": "1000000044888d311"
# }
def save(topic, message):
    """
    Saves a JSON message to the MongoDB log collection.

    :param topic: The topic for the log (string)
    :param message: The JSON message containing log details
    """
    if isinstance(message, str):
        message = json.loads(message)
    print(message)
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]

        # Convert the message into the correct format
        message["_id"] = ObjectId()  # Generate a new ObjectId for the document
        message["date_log"] = datetime.fromisoformat(message["date_log"].replace("Z", "+00:00"))

        # Insert the log entry into the collection
        result = collection.insert_one(message)
        # print("Log entry saved successfully with ID:", result.inserted_id)

    except Exception as e:
        print("An error occurred while saving the log:", e)

def print_table():
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]

        # Fetch all documents from the collection
        documents = collection.find()

        # Create a PrettyTable instance
        table = PrettyTable()
        table.field_names = ["_id", "topic", "date_log", "value_log", "id_premise", "id_device"]

        # Add rows to the table
        for doc in documents:
            table.add_row([
                str(doc.get("_id", "")),
                doc.get("topic", ""),
                doc.get("date_log", ""),
                doc.get("value_log", ""),
                doc.get("id_premise", ""),
                doc.get("id_device", "")
            ])

        # Print the table
        print(table)

    except Exception as e:
        print("An error occurred:", e)

def get_logs(query):
    try:
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]
        
        # If a query is provided, filter logs based on it (case-insensitive search)
        if query:
            logs = list(collection.find({
                "$or": [
                    {"topic": {"$regex": query, "$options": "i"}},
                    {"value_log": {"$regex": query, "$options": "i"}},
                    {"id_premise": {"$regex": query, "$options": "i"}},
                    {"id_device": {"$regex": query, "$options": "i"}},
                ]
            }).sort("date_log", -1))  # Newest logs first
        else:
            logs = list(collection.find().sort("date_log", -1))  # Fetch all logs if no query is provided

        return logs
    except Exception as e:
        print("An error occurred while fetching logs:", e)
        return []
# Example usage
# if __name__ == "__main__":
#     topic = "smartoffice/log"
#     message = {
#         "_id": 1,  # This will be replaced with a generated ObjectId
#         "topic": topic,
#         "date_log": "2024-12-25T09:15:00Z",
#         "value_log": "0000AEC6680",
#         "id_premise": "1",
#         "id_device": "1000000044888d311"
#     }

#     save(topic, message)
#     print_table()

