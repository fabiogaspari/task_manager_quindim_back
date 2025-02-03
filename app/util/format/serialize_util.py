from bson import ObjectId

def objectid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError("Tipo não serializável.")