/*global Backbone */
var app = app || {};

(function () {
	'use strict';

	var Blueprints = Backbone.Collection.extend({
		model: app.Blueprint,
		url: "/blueprints/search",
		total: 0,
		parse: function(data) {
		    this.total = data.count
		    return data.items
		},
		getOrFetch: function(id, options) {
		    var mdl = this.get(id)
		    if (mdl) options.success(mdl)
		    else this.add({id: id}).fetch(options)
		},
		fetchTypes: function() {
		    return $.ajax({url: "/blueprints/types", method: "GET"})
		},
		load: function() {
		    this.fetch({reset: true, method: "POST", data: JSON.stringify({
		        limit: 12, query: {and: []}
		    })})
		}
	})

	app.blueprints = new Blueprints();
})();
