import firebase_admin
from firebase_admin import credentials, firestore, storage, db
import os

cred=credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'silocheck-ea58e.appspot.com' ,
    'databaseURL': 'https://silocheck-ea58e-default-rtdb.europe-west1.firebasedatabase.app'
})

bucket = storage.bucket()
ref = db.reference('/')
home_ref = ref.child('silo_data')

def push_db(temperature,level, time):
  # Push file reference to image in Realtime DB
  home_ref.push({
      'temperature': temperature,
      'level':level,
      'timestamp': time}
  )
