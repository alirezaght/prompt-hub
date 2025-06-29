from firebase import db
from firebase_admin.firestore import firestore
from datetime import timedelta

def put_to_cache(key: str, value: dict, expiration: int = 3600):
    """
    Store a value in the cache with an expiration time.
    
    :param key: The key under which to store the value.
    :param value: The value to store, must be serializable to JSON.
    :param expiration: Time in seconds after which the cache entry expires.
    """
    db.collection('cache').document(key).set({
        'value': value,
        'expiration': firestore.SERVER_TIMESTAMP + timedelta(seconds=expiration)
    })
    
def get_from_cache(key: str):
    """
    Retrieve a value from the cache.
    
    :param key: The key of the cached value.
    :return: The cached value if it exists and is not expired, otherwise None.
    """
    doc = db.collection('cache').document(key).get()
    if doc.exists:
        data = doc.to_dict()
        if 'expiration' in data and data['expiration'] > firestore.SERVER_TIMESTAMP:
            return data['value']
    return None