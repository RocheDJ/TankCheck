"use strict";

const express = require("express");
const router = express.Router();
const farm = require('./controllers/farm.js');


const dashboard = require("./controllers/dashboard.js");
const about = require("./controllers/about.js");


router.get("/", dashboard.index);
router.get("/dashboard", dashboard.index);
router.get('/farm/:id', farm.index);
router.get("/about", about.index);

module.exports = router;
