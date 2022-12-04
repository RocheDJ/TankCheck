"use strict";

const logger = require("../utils/logger");
const farmStore = require('../models/farm-store');

//const myFarms = [{name:"Medow Farm", silos:"1"},{name:"Dale Farm", silos:"1"},{name:"Hillview Ltd", silos:"2"}];
const dashboard = {
  index(request, response) {
    logger.info("dashboard rendering");

   // const myFarms = farmStore.getUserStationsSorted(loggedInUser.id);
    const myFarms = farmStore.getAllFarms();
    const viewData = {
      title: "Silo check Dashboard",
      farms: myFarms,
    };
    response.render("dashboard", viewData);
  },
};

module.exports = dashboard;
