from firebase import db
from firebase_admin.firestore import firestore
from datetime import timedelta, datetime, timezone

def put_to_cache(key: str, value: dict, expiration: int = 3600):
    """
    Store a value in the cache with an expiration time.
    
    :param key: The key under which to store the value.
    :param value: The value to store, must be serializable to JSON.
    :param expiration: Time in seconds after which the cache entry expires.
    """    
    expiration_dt = datetime.now(timezone.utc) + timedelta(seconds=expiration)
    db.collection('cache').document(key).set({
        'value': value,
        'expiration': expiration_dt
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
        if 'expiration' in data and data['expiration'] > datetime.now(timezone.utc):
            return data['value']
        else:
            # Cache entry has expired, remove it
            db.collection('cache').document(key).delete()
    return None