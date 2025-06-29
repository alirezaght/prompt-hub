import firebase_admin
from firebase_admin import credentials, storage, firestore
import json
# -- Firebase Setup --
import os
firebase_creds = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON")
if firebase_creds:
    cred = credentials.Certificate(json.loads(firebase_creds))
elif os.path.exists("firebase-service-account.json"):
    cred = credentials.Certificate("firebase-service-account.json")
else:
    raise ValueError("Firebase credentials not found. Set FIREBASE_SERVICE_ACCOUNT_JSON env var or place firebase-service-account.json in the current directory.")

firebase_admin.initialize_app(cred, {    
    "storageBucket": "prompt-hub-2bdbf.firebasestorage.app"
})
bucket = storage.bucket()

db = firestore.client()
