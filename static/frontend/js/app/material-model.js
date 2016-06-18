/*global Backbone */
var app = app || {};

(function () {
	'use strict';

	app.Material = Backbone.Model.extend({
		defaults: {
			title: '',
			locations: 'unknown',
			tracked: false,
			quantity: 0,
			inventory: 0,
		},
		urlRoot: "/materials"
	});
})();
