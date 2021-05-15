from ..utils.constants import SERVICE_ACCOUNT_KEY
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore as firebase_firestore
import os, json

serviceAccountKeys = json.loads(os.environ.get(SERVICE_ACCOUNT_KEY))
cred = credentials.Certificate(serviceAccountKeys)
firebase_admin.initialize_app(cred)

db = firebase_firestore.client()
firestore = firebase_firestore
