/*global Backbone */
var app = app || {};

(function () {
	'use strict';

	app.InvMaterial = Backbone.Model.extend({
	    defaults: {
	        id: null,
	        quantity: 0
	    },
	    quantityPlus: function(value) {
	        var q = this.get("quantity")
	        q += value
	        this.save({quantity: q})
	    }
	})

	var MaterialInventory = Backbone.Collection.extend({
		model: app.InvMaterial,
		localStorage: new Backbone.LocalStorage("InvMaterial")
	})

	app.inventory = new MaterialInventory()
})()
