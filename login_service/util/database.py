from datetime import datetime

from bson import ObjectId
from pymongo import MongoClient


class DatabaseHandler(object):

    def __init__(self):
        self.conn = MongoClient().Pollote

    def insert(self, element, collection_name):
        element["created_date"] = datetime.now()
        element["updated_date"] = datetime.now()
        inserted = self.conn[collection_name].insert_one(element)
        return str(inserted.inserted_id)

    def find(self, criteria, collection_name, projection=None, sort=None, limit=0, cursor=False):
        if "_id" in criteria:
            criteria["_id"] = ObjectId(criteria["_id"])
        found = self.conn[collection_name].find(filter=criteria, projection=projection, limit=limit, sort=sort)
        if cursor:
            return found
        found = list(found)
        for i in range(len(found)):  # to serialize object id need to convert string
            if "_id" in found[i]:
                found[i]["_id"] = str(found[i]["_id"])
        return found

    def find_by_id(self, id, collection_name):
        found = self.conn[collection_name].find_one({"_id": ObjectId(id)})
        if found is None:
            return not found
        if "_id" in found:
            found["_id"] = str(found["_id"])
        return found

    def update(self, id, element, collection_name):
        criteria = {"_id": ObjectId(id)}
        element["updated"] = datetime.now()
        set_obj = {"$set": element}  # update value
        updated = self.conn[collection_name].update_one(criteria, set_obj)
        if updated.matched_count == 1:
            return "Record Successfully Updated"

    def delete(self, id, collection_name):
        deleted = self.conn[collection_name].delete_one({"_id": ObjectId(id)})
        return bool(deleted.deleted_count)
