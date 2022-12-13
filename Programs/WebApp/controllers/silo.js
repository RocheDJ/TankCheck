"use strict";

const logger = require("../utils/logger");
const fireDB = require('../Data/fireDBInterface.js');
const uuid = require("uuid");
const LocalDateTime = require("lodash");
const axios = require("axios"); //npm install axios
const sortArrayOfObjects = require("../utils/sort");

function padWithZero(num, targetLength) {
  return String(num).padStart(targetLength, "0");
}

const silo = {
  index(request, response) {
    const siloId = request.params.id;
    const mySilo = fireDB.fireDBInterface.getSilo(siloId)
    logger.debug("Silo id = ", siloId);
    //sort the data for each station in order for trend graph
     mySilo.readings = sortArrayOfObjects(mySilo.readings,"epocDate","asec");
    const viewData = {
      name: "Silo",
      silo: mySilo
    };
    response.render("silo", viewData);
  },

  deleteReading(request, response) {
    const stationId = request.params.id;
    const readingId = request.params.readingid;
    logger.debug(`Deleting Reading ${readingId} from Station ${stationId}`);
    stationStore.removeReading(stationId, readingId);
    response.redirect("/station/" + stationId);
  },

  addReading(request, response) {
    const stationId = request.params.id;
    let station = stationStore.getStation(stationId);
    let now = LocalDateTime.now();
    const DateUTC = new Date(now).toUTCString();
    const sDate = (new Date(DateUTC).getFullYear() + "-" + padWithZero(new Date(DateUTC).getMonth(), 2) + "-" + padWithZero(new Date(DateUTC).getDate(), 2)
      + " " + padWithZero(new Date(DateUTC).getHours(), 2) + ":" + padWithZero(new Date(DateUTC).getMinutes(), 2) + ":" + padWithZero(new Date(DateUTC).getSeconds(), 2));
    const newReading = {
      id: uuid.v1(),
      code: Number(request.body.code),
      temperature: Number(request.body.temperature),
      pressure: Number(request.body.pressure),//Number converts the string to a number
      windSpeed: Number(request.body.windSpeed),//Number converts the string to a number
      windDirection: Number(request.body.windDirection),//Number converts the string to a number
      readingDate: sDate,
      epocDate: now
    };

    stationStore.addReading(stationId, newReading);
    logger.debug("New Reading = ", newReading);
    response.redirect("/station/" + stationId);
  },

  async addAutoReading(request, response) {
    const stationId = request.params.id;
    const station = stationStore.getStation(stationId);
    const api_url = "https://api.openweathermap.org/data/2.5/weather?lat=" + station.latitude + "&lon=" + station.longitude + "&appid=25b8dadd1f0eaed0dd4707048527a093" + "&units=metric";
    logger.info("rendering new report");

    let now = LocalDateTime.now();
    const DateUTC = new Date(now).toUTCString();
    const sDate = (new Date(DateUTC).getFullYear() + "-" + padWithZero(new Date(DateUTC).getMonth(), 2) + "-" + padWithZero(new Date(DateUTC).getDate(), 2)
      + " " + padWithZero(new Date(DateUTC).getHours(), 2) + ":" + padWithZero(new Date(DateUTC).getMinutes(), 2) + ":" + padWithZero(new Date(DateUTC).getSeconds(), 2));

    const result = await axios.get(api_url);
    if (result.status === 200) {
      const reading = result.data;
      const newReading = {
        id: uuid.v1(),
        code: Number(reading.cod),
        temperature: Number(reading.main.temp),
        pressure: Number(reading.main.pressure),//Number converts the string to a number
        windSpeed: Number(reading.wind.speed),//Number converts the string to a number
        windDirection: Number(reading.wind.deg),//Number converts the string to a number
        readingDate: sDate,
        epocDate: now,
      };
      stationStore.addReading(stationId, newReading);
      logger.debug("New Reading = ", newReading);
    }
    response.redirect("/station/" + stationId);
  }
};

module.exports = silo;