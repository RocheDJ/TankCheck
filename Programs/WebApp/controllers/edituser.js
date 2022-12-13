"use strict";

const logger = require("../utils/logger");
const accounts = require("./accounts");

const edituser = {
  index(request, response) {
    logger.info("edit user rendering");
    const loggedInUser = accounts.getCurrentUser(request);
    const viewData = {
      title: "Edit user information",
      firstName: loggedInUser.firstName,
      lastName: loggedInUser.lastName,
      email:loggedInUser.email
    };
    response.render("edituser", viewData);
  }
};

module.exports = edituser;