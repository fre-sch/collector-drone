/*global $ */
/*jshint unused:false */
var app = app || {}
var ENTER_KEY = 13
var ESC_KEY = 27

$(function () {
	'use strict'

	$.ajaxSetup({
	    contentType: "application/json"
	})

	new app.AppView()
});
