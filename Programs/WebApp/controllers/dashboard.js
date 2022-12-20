"use strict";
const logger = require("../utils/logger");
const fireDB = require('../Data/fireDBInterface.js');
const accounts = require ('./accounts.js');

fireDB.fireDBInterface.connectFarm();
fireDB.fireDBInterface.connectSilo();

const dashboard = {
   index(request, response) {
   logger.info("dashboard rendering");
   const loggedInUser = accounts.getCurrentUser(request);
   const myFarms = fireDB.fireDBInterface.getFarms();
   // const myFarms = farmStore.getUserStationsSorted(loggedInUser.id);

   const viewData = {
       title: "Silo Check Dashboard",
       farms   : myFarms,
     };
   response.render("dashboard", viewData);
 },
  setOn(request, response){
    const siloId = request.params.id;
    fireDB.fireDBInterface.setSiloAgitatorOn(siloId);
    response.redirect("/dashboard");

  },
  setOff(request, response){
    const siloId = request.params.id;
    fireDB.fireDBInterface.setSiloAgitatorOff(siloId);
    response.redirect("/dashboard");

  }
};

module.exports = dashboard;
