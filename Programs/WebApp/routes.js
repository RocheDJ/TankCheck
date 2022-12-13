"use strict";

const express = require("express");
const router = express.Router();
const accounts = require('./controllers/accounts.js');
const edituser = require('./controllers/edituser.js');
const dashboard = require("./controllers/dashboard.js");
const about = require("./controllers/about.js");
const silo = require("./controllers/silo.js");

router.get('/', accounts.index);
router.get('/login', accounts.login);
router.get('/signup', accounts.signup);
router.get('/logout', accounts.logout);
router.post('/register', accounts.register);
router.post('/authenticate', accounts.authenticate);
router.post('/updateUser', accounts.updateUser);
router.get('/edituser', edituser.index);

//router.get("/", dashboard.index);

router.get("/dashboard", dashboard.index);
router.get('/dashboard/setOn/:id', dashboard.setOn);
router.get('/dashboard/setOff/:id', dashboard.setOff);
router.get('/silo/:id', silo.index);
router.get("/about", about.index);

module.exports = router;
