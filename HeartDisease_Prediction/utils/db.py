import os
from typing import Any, Dict, List, Optional

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConfigurationError, ConnectionFailure, ServerSelectionTimeoutError

DEFAULT_DB_NAME = "heart_prediction"
DEFAULT_COLLECTION_NAME = "patients"


def get_mongo_uri() -> str:
    return os.getenv("MONGODB_URI", "")


def get_client(uri: str) -> Optional[MongoClient]:
    if not uri:
        return None

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        client.server_info()
        return client
    except (ConfigurationError, ServerSelectionTimeoutError, ConnectionFailure):
        return None


def get_patient_collection(
    uri: str,
    db_name: str = DEFAULT_DB_NAME,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> Optional[Collection]:
    client = get_client(uri)
    if client is None:
        return None
    return client[db_name][collection_name]


def convert_objectid(document: Dict[str, Any]) -> Dict[str, Any]:
    if "_id" in document:
        document["id"] = str(document["_id"])
        document.pop("_id", None)
    return document


def create_patient_record(collection: Collection, record: Dict[str, Any]) -> str:
    inserted = collection.insert_one(record)
    return str(inserted.inserted_id)


def list_patient_records(collection: Collection, filter_query: Optional[Dict[str, Any]] = None, limit: int = 200) -> List[Dict[str, Any]]:
    if filter_query is None:
        filter_query = {}
    cursor = collection.find(filter_query).limit(limit)
    return [convert_objectid(doc) for doc in cursor]


def search_patient_records(collection: Collection, search_text: str, limit: int = 200) -> List[Dict[str, Any]]:
    if not search_text:
        return list_patient_records(collection, limit=limit)

    regex = {"$regex": search_text, "$options": "i"}
    filter_query = {
        "$or": [
            {"name": regex},
            {"gender": regex},
            {"diagnosis": regex},
            {"medical_history": regex},
            {"notes": regex},
        ]
    }
    return list_patient_records(collection, filter_query=filter_query, limit=limit)


def update_patient_record(collection: Collection, patient_id: str, updates: Dict[str, Any]) -> bool:
    result = collection.update_one({"_id": ObjectId(patient_id)}, {"$set": updates})
    return result.matched_count > 0


def delete_patient_record(collection: Collection, patient_id: str) -> bool:
    result = collection.delete_one({"_id": ObjectId(patient_id)})
    return result.deleted_count > 0
