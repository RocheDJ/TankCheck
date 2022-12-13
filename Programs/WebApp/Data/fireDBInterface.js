"use strict";
const firebase = require("firebase/compat/app");
const db = require("firebase/compat/database");
const uuid = require("uuid");
const logger = require("../utils/logger");
const sortArrayOfObjects = require("../utils/sort");

const firebaseConfig = {
  apiKey: "AIzaSyA9VlIuYkEOyuXXLZWayP_KuVbTKOWTDHY",
  authDomain: "silocheck-ea58e.firebaseapp.com",
  databaseURL: "https://silocheck-ea58e-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "silocheck-ea58e",
  storageBucket: "silocheck-ea58e.appspot.com",
  messagingSenderId: "987989013018",
  appId: "1:987989013018:web:63a865cbc3856cb23cd7a3"
};

firebase.initializeApp(firebaseConfig);

const firebaseDB = firebase.database();

let farmArray = [];
let siloArray = [];

const fireDBInterface = {

  connectFarm() {
    firebaseDB.ref("farm").on("value",
      function(snapshot) {
        farmArray.length = 0;
        snapshot.forEach(function(childSnapshot) {
            farmArray.push(childSnapshot.val());
            logger.info("Farm loaded: ");
          }
        );
      });
  },
  connectSilo() {
    firebaseDB.ref("silo").on("value",
      function(snapshot) {
        siloArray.length = 0;
        snapshot.forEach(function(childSnapshot) {
          siloArray.push(childSnapshot.val());
          farmArray[0].silos[0] = childSnapshot.val();
          farmArray[0].silos[0].readings = sortArrayOfObjects(farmArray[0].silos[0].readings, "epocDate");
          logger.info("Silo loaded: ");

        });
      });
  },
//- Functions to be accessed from web app
  getFarms() // return the farm array
  {
    return farmArray;
  },

  getSilos()// return the silo array
  {
    const silos = siloArray;// get all stations for user in order as displaied
    let siloreadings = [];
    for (let iX = 0; iX < silos.length; iX++) {
      let readings = silos[iX].readings;
      if (readings) {
        let allSiloReadings = sortArrayOfObjects(readings, "epocDate");
        let currentReading = allSiloReadings[allSiloReadings.length - 1];
        if (currentReading) {
          siloreadings.push(currentReading);
        }
        siloArray[iX].readings = allSiloReadings;
      } else {
        siloreadings.push([]);
      }
    }
    return this.siloArray;
  },

  getSilo(siloID)// return the silo requested with its readings in cron order
  {
    const silos = siloArray;
    var  silo;
    for (let iX = 0; iX < silos.length; iX++) {
      if (silos[iX].config.siloID == siloID) {
        silo =silos[iX];
      }
      return silo;
    }
  },
  setSiloAgitatorOn(siloID)// return the silo requested with its readings in cron order
  {
    firebaseDB.ref("silo/"+siloID+"/config").update({ control:"ON"});
  },
  setSiloAgitatorOff(siloID)// return the silo requested with its readings in cron order
  {
    firebaseDB.ref("silo/"+siloID+"/config").update({ control:"OFF"});
  }
};
module.exports = {
  fireDBInterface
};