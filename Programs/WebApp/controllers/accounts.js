'use strict';

const userstore = require('../models/user-store');
const logger = require('../utils/logger');
const uuid = require('uuid');

const accounts = {

  index(request, response) {
    const viewData = {
      title: 'Login or Signup',
    };
    response.render('index', viewData);
  },

  login(request, response) {
    const viewData = {
      title: 'Login to the Service',
    };
    response.render('login', viewData);
  },

  logout(request, response) {
    response.cookie('station', '');
    response.redirect('/');
  },

  signup(request, response) {
    const viewData = {
      title: 'Login to the Service',
    };
    response.render('signup', viewData);
  },

  register(request, response) {
    const user = request.body;
    user.id = uuid.v1();
    userstore.addUser(user);
    logger.info(`registering ${user.email}`);
    response.redirect('/');
  },

  authenticate(request, response) {
    const user = userstore.getUserByEmail(request.body.email);
    const enteredpassword = request.body.password;
    if (user) {
      if (user.password ===  enteredpassword){
        response.cookie('station', user.email);
        logger.info(`logging in ${user.email}`);
        response.redirect('/dashboard');
      }else {
        response.redirect('/login');
      }
    } else {
      response.redirect('/login');
    }
  },

  getCurrentUser(request) {
    const userEmail = request.cookies.station;
    return userstore.getUserByEmail(userEmail);
  },

  updateUser(request,response){
    const userEmail = request.cookies.station;
    const user = userstore.getUserByEmail(request.body.email);
    const userid = user.id;

    const firstName = request.body.firstName
    const lastName = request.body.lastName
    const email = request.body.email
    const password = user.password;
    const oldpassword = request.body.oldpassword
    const newpassword = request.body.newpassword
    const confirmpassword = request.body.confirmpassword

    if (oldpassword==password){
      if(newpassword==confirmpassword) {
        logger.info(`updating info for  ${user.email}`);
        userstore.updateUserById(userid,firstName,lastName,email,newpassword);
        response.redirect('/dashboard');
      }else{
        response.redirect('/edituser');
      }
    } else{
      response.redirect('/edituser');
    }

  }

};

module.exports = accounts;