/*global Backbone */
var app = app || {};

(function () {
    'use strict';

    var TrackBlueprint = Backbone.Model.extend({
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

    /*
    new app.TrackMaterialView({model: {
        inventory: inventoryModel
        trackBlueprint: trackBlueprint
        ingredient: ingredientObject
    }})
    */
	app.TrackMaterialView = Backbone.View.extend({
	    template: _.template($('#track-material-tpl').html()),
	    className: "col-md-6",
		events: {
		    "click .inventory-plus": "inventoryPlus",
		    "click .inventory-minus": "inventoryMinus"
		},
		initialize: function(options) {
		    app.trackingFilter.plus("numMaterials", 1)
			this.listenTo(this.model.inventory, 'change', this.render)
			this.listenTo(this.model.trackBlueprint, "change", this.render)
			this.listenTo(this.model.trackBlueprint, 'destroy', this.remove)
			this.listenTo(this.model.trackBlueprint, 'destroy', this.updateTrackingFilter)
		},
		render: function() {
		    var data = {
		        quantity: this.model.trackBlueprint.get("quantity") * this.model.ingredient.quantity,
		        inventory: this.model.inventory.get("quantity"),
		        material: this.model.ingredient.material
		    }
			this.$el.html(this.template(data))
			return this
		},
		updateTrackingFilter: function() {
		    app.trackingFilter.plus("numMaterials", -1)
		},
		inventoryPlus: function() { this.model.inventory.quantityPlus(1) },
		inventoryMinus: function() { this.model.inventory.quantityPlus(-1) }
	})

    /*
    new app.TrackBlueprintView({model: {
        trackBlueprint: trackBlueprint,
        blueprint: blueprint
    }})
    */
    app.TrackBlueprintView = Backbone.View.extend({
        template: _.template($('#blueprint-tpl').html()),
        className: "col-md-6",
        events: {
            "click .track": "track",
            "click .remove": "untrack",
            "click .craft": "craft"
        },
        initialize: function() {
            this.listenTo(this.model.trackBlueprint, 'change', this.render)
            this.listenTo(this.model.trackBlueprint, 'destroy', this.remove)
        },
        render: function() {
            var data = _.extend(
                this.model.trackBlueprint.toJSON(),
                this.model.blueprint.toJSON()
            )
            data.tracked = true
            this.$el.html(this.template(data))
            return this
        },
        track: function() {
            this.model.trackBlueprint.quantityPlus(1)
        },
        untrack: function() {
            this.model.trackBlueprint.destroy()
        },
        craft: function() {
            this.model.trackBlueprint.quantityPlus(-1)
            if (this.model.trackBlueprint.get("quantity") <= 0) {
                this.untrack()
            }
        }
    })

    var TrackingCollection = Backbone.Collection.extend({
        model: TrackBlueprint,
        localStorage: new Backbone.LocalStorage("trackBlueprint")
    })

    app.tracking = new TrackingCollection()
})()
