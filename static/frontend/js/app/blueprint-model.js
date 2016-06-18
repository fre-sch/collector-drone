/*global Backbone */
var app = app || {};

(function () {
	'use strict';

	app.Blueprint = Backbone.Model.extend({
		defaults: {
			title: '',
			ingredients: [],
			engineers: {},
			tracked: false
		},
		urlRoot: "/blueprints"
	});
})();
