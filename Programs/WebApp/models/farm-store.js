"use strict";
const _ = require("lodash");
const JsonStore = require("./json-store");
const sortArrayOfObjects = require("../utils/sort");
// const stationUtils = require("../utils/stationUtils");

// ####################### FIREBASE ########################################################
// Your web app's Firebase configuration

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

// Get a reference to the file storage service
const storage = firebase.storage();
// Get a reference to the database service
const database = firebase.database();

// ####################### FIREBASE ########################################################

const farmStore = {

  store: new JsonStore("./models/farm-store.json", { farmCollection: [] }),
  collection: "farmCollection",

  getAllFarms() {
    return this.store.findAll(this.collection);
  },

  getFireTest() {
    return this.store.findAll(this.collection);
  },


  getFarm(id) {
    return this.store.findOneBy(this.collection, { id: id });
  },

  addFarm(station) {
    this.store.add(this.collection, station);
    this.store.save();
  },

  removeFarm(id) {
    const farm = this.getStation(id);
    this.store.remove(this.collection, farm);
    this.store.save();
  },

  removeAllFarms() {
    this.store.removeAll(this.collection);
    this.store.save();
  },

  updateCurrentValues(id){
    const farm = this.getFarm(id);
    const readingsDesc = sortArrayOfObjects(station.readings,"","desc"); // sort in descending latest date is in index 0
    const recentReading =readingsDesc[0];
    farm.current_temp_c = recentReading.temperature.toFixed(1);
  },

  addReading(id, reading) {
    const farm = this.getFarm(id);
    farm.readings.push(reading);
    this.updateCurrentValues(id);
    this.store.save();
  },

  removeReading(id, readingId) {
    const farm = this.getStation(id);
    const readings = farm.readings;
    _.remove(readings, { id: readingId });
    this.updateCurrentValues(id);
    this.store.save();
  },

  getUserFarms(userid) {
    return this.store.findBy(this.collection, { userid: userid });
  },

  getUserfFarmsSorted(userid) {
    const retFarms = this.getUserFarms(userid);
    return sortArrayOfObjects(retFarms, "name");
  },

  // return the last updated reading for this Farm
  getFarmsCurrentData(userid) {
    const farms = this.getUserfFarmsSorted(userid);// get all stations for user in order as displaied

    let farmreadings = [];
    for (let iX = 0; iX < farms.length; iX++) {
      let readings = farms[iX].readings;
      if (readings) {
        let allStationreadings = sortArrayOfObjects(readings, "date");// go through the statins and get the current readings
        let currentReading = allStationreadings[allStationreadings.length - 1];
        if (currentReading) {
          farmreadings.push(currentReading);
        }
      } else {
        farmreadings.push([]);
      }
    }
    return farmreadings;
  }

};

module.exports = farmStore;