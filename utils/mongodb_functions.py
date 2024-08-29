from pymongo import MongoClient
from bson.objectid import ObjectId

from bson.json_util import dumps

def check_email(uri, database_name, collection_name, email):
    # Establish a connection to the MongoDB database
    client = MongoClient(uri)
    db = client[database_name]
    collection = db[collection_name]

    # Search for a document where the email field matches the given email
    existing_document = collection.find_one({"email": email})

    if existing_document:
        print(existing_document)
        # If the document exists, return the document
        return dumps(existing_document), "found"
    else:
        # If the document does not exist, return just the email and "not_found" status
        new_document = {"email": email}  # Prepare a new document structure if needed
        return dumps(new_document), "not_found"
    


def update_document(uri, database_name, collection_name, user_id_str, company, date_time):
    client = MongoClient(uri)
    db = client[database_name]
    collection = db[collection_name]

    try:
        user_id = ObjectId(user_id_str)  # Convert the string ID to ObjectId
    except Exception as e:
        print(f"Error converting ID to ObjectId: {e}")
        return 0  # Return 0 updates if conversion fails

    print(f"Converted ObjectId: {user_id}")
    print(f"Company: {company}")
    print(f"Date-Time: {date_time}")

    # Prepare the update details
    filter_query = {"_id": user_id}
    update_data ={"$push": {
        "history": {
            "$each": [{"company": company, "date": date_time}],
            "$position": 0  # This adds the new element at the start of the array
        }}
    }

    print(f"Filter: {filter_query}")
    print(f"Update Data: {update_data}")

    # Update operation
    try:
        result = collection.update_one(filter_query, update_data)
        print(f"Modified Count: {result.modified_count}")
        return result.modified_count
    except Exception as e:
        print(f"Update failed: {e}")
        return 0  # Indicate failure with 0 modified count


def create_document(uri,database_name,collection_name,email,name,company,date_time):

    client = MongoClient(uri)
    db = client[database_name]
    collection = db[collection_name]

    new_document = {
            "email": email,
            "name": name,
            "history": [
                {"company": company, "date": date_time}
            ]
        }
    result = collection.insert_one(new_document)
    return result.inserted_id