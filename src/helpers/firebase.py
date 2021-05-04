import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

cred = credentials.Certificate("src/creds/service_account_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()