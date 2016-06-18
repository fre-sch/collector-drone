/*global Backbone */
var app = app || {};

(function () {
	'use strict';

	var Materials = Backbone.Collection.extend({
		model: app.Material,
		url: "/materials/search",
		total: 0,
		parse: function(data) {
		    this.total = data.count
		    return data.items
		},
		fetchOne: function(id, options) {
		    var mdl = this.add({id: id})
		    mdl.fetch(options)
		    return mdl
		},
		load: function() {
		    this.fetch({reset: true, method: "POST", data: JSON.stringify({
		        limit: 12, query: {and: []}
		    })})
		}
	})

	app.materials = new Materials()
})()
