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

def read_agitator(siloID):
  agitatorSP = ref.child('silo/1001/config/control').get()
  if str(agitatorSP) == "OFF":
     return False   
  else:
     return True  
      
def push_db(deviceID,temperature,level, time):
  # home_ref = ref.child('silo_data')
  home_ref = ref.child(deviceID)
  # Push file reference to image in Realtime DB
  home_ref.push({
      'temperature': temperature,
      'level':level,
      'timestamp': time}
  )

# push up the local configuration for the silo to the Web app
def push_db_silo(siloID,
                iMax_mm,iMin_mm,
                iMax_ltr,iMin_ltr,
                sProduct):
  home_ref = ref.child('silo/' + siloID+"/config")
  home_ref.update({
      'siloID'  : siloID,
      'max_mm'  : iMax_mm,
      'min_mm'  : iMin_mm,
      'max_ltr' : iMax_ltr,
      'min_ltr' : iMin_ltr,
      'product' : sProduct
     }
  )
  home_ref = ref.child('silo/' + siloID+"/config")
  home_ref.update({ 'control' : 'OFF'})

# push up the readings up to the database
def push_db_silo_reading(siloID,iReadcount,
                fTemperature,iLevel,
                xActuater,sTime,
                eDateTime):

  home_ref = ref.child('silo/' + siloID +'/readings/'+ str(iReadcount)) 
  home_ref.update({
      'temperature'  : fTemperature,
      'level_mm'  : iLevel,
      'actuator_state' : xActuater,
      'timestamp' : sTime,
      'epocDate' :eDateTime 
     }
  )