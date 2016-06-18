/*global Backbone, jQuery, _, ENTER_KEY */
var app = app || {};

(function ($) {
	'use strict';

	var TrackingFilter = Backbone.Model.extend({
	    defaults: {
	        numBlueprints: 0,
	        numMaterials: 0
	    },
	    initialize: function() {
	        this.listenTo(app.tracking, "add", this.updateQuantities)
	        this.listenTo(app.tracking, "remove", this.updateQuantities)
	        this.listenTo(app.tracking, "reset", this.updateQuantities)
	    },
	    updateQuantities: function() {
	        this.set("numBlueprints", app.tracking.length)
	    },
	    plus: function(attribute, value) {
	        var t = this.get(attribute)
	        t += value
	        this.set(attribute, t)
	        return t
	    }
	})
	app.trackingFilter = new TrackingFilter()

	var TrackTabView = Backbone.View.extend({
	    el: "#track-tab-view",
	    events: {
	        "click a": "showTab"
	    },
	    initialize: function() {
	        this.$numBlueprints = this.$el.find(".numBlueprints")
	        this.$numMaterials = this.$el.find(".numMaterials")
	        this.listenTo(app.trackingFilter, "change", this.updateQuantities)
	    },
	    showTab: function(event) {
	        var $target = $(event.target)
            this.$el.find("a").each(function() {
                $($(this).data("tab")).hide()
            })
            this.$el.children("li").removeClass("active")
	        $($target.data("tab")).show()
	        $target.parent().addClass("active")
	    },
	    updateQuantities: function() {
	        this.$numBlueprints.html(app.trackingFilter.get("numBlueprints"))
	        this.$numMaterials.html(app.trackingFilter.get("numMaterials"))
	    }
	})
	app.trackTabView = new TrackTabView()

	app.AppView = Backbone.View.extend({
	    el: 'body',
	    events: {
	    },
		initialize: function () {
	        this.catalogs = {
	            blueprints: $("#catalog-blueprints"),
	            materials: $("#catalog-materials"),
	            engineers: $("#catalog-engineers")
	        }
            this.$trackMaterials = $('#track-materials')
            this.$trackBlueprints = $('#track-blueprints')

            this.listenTo(app.catalogFilter, "change:search change:type", this.catalogFilterChanged)
            this.listenTo(app.blueprints, 'reset', this.onBlueprintsReset)
            this.listenTo(app.materials, 'reset', this.onMaterialsReset)
            this.listenTo(app.tracking, 'add', this.addTrackingView)
            this.listenTo(app.tracking, "reset", this.onTrackingReset)

            app.blueprints.fetchTypes()
                .done(function(blueprintTypes) {
                    _.each(blueprintTypes.items,
                        app.catalogFilterView.addFilterItem,
                        app.catalogFilterView)
                })
            app.blueprints.load()
            app.materials.load()
            app.inventory.fetch({reset: true})
            app.tracking.fetch({reset: true})
		},

		onBlueprintsReset: function(collection, options) {
		    this.catalogs.blueprints.empty()
		    collection.each(this.createBlueprintView, this)
		},

		onMaterialsReset: function(collection, options) {
		    var that = this
		    this.catalogs.materials.empty()
		    collection.each(this.createMaterialView, this)
		},

		onTrackingReset: function(collection, options) {
		    collection.each(function(trackBlueprint) {
		        this.addTrackingView(trackBlueprint)
            }, this)
		},

		createBlueprintView: function (blueprint) {
			var view = new app.BlueprintView({model: blueprint})
	        var el = view.render().el
			this.catalogs.blueprints.append(el)
		},

		createMaterialView: function (material) {
			var view = new app.MaterialView({model: material})
	        var el = view.render().el
			this.catalogs.materials.append(el)
		},

		addOneTrackMaterial: function(trackMaterial) {
		    var createViewAndAppend = _.bind(function(track, material) {
                var view = new app.TrackMaterialView({
                    model: track,
                    material: material
                })
                this.$trackMaterials.append(view.render().el)
		    }, this, trackMaterial)

		    var material = app.materials.get(trackMaterial.id)
		    if (material) {
		        createViewAndAppend(material)
		    }
		    else {
		        app.materials.add({id: trackMaterial.id})
		            .fetch({success: createViewAndAppend})
		    }
		},

		addTrackingView: function(trackBlueprint) {
		    var createViewAndAppend = _.bind(function(trackBlueprint, blueprint) {
		        this.addTrackBlueprintView(trackBlueprint, blueprint)
		        _.each(blueprint.get("ingredients"), function(ingredient) {
                    this.addTrackMaterialView(trackBlueprint, ingredient)
                }, this)
		    }, this, trackBlueprint)
		    app.blueprints.getOrFetch(trackBlueprint.id, {
		        success: createViewAndAppend
            })
		},

        addTrackBlueprintView: function(trackBlueprint, blueprint) {
            var view = new app.TrackBlueprintView({model: {
                trackBlueprint: trackBlueprint,
                blueprint: blueprint,
            }})
            this.$trackBlueprints.append(view.render().el)
        },

        addTrackMaterialView: function(trackBlueprint, ingredient) {
            var inventory = app.inventory.get(ingredient.material.id)
            if (!inventory)
                inventory = app.inventory.create({
                    id: ingredient.material.id,
                    quantity: 0
                })
            var view = new app.TrackMaterialView({model: {
                inventory: inventory,
                trackBlueprint: trackBlueprint,
                ingredient: ingredient
            }})
            this.$trackMaterials.append(view.render().el)
        },

		catalogFilterChanged: function(catalogFilter, options) {
		    if (catalogFilter.get("category") == "blueprints") {
		        console.info("catalogFilterChanged", catalogFilter.attributes)
                app.blueprints.fetch({reset: true, method: "POST",
                    data: JSON.stringify({
                        limit: 12,
                        query: catalogFilter.getQuery()
                    })
                })
            }
            else if (catalogFilter.get("category") == "materials") {
                app.materials.fetch({reset: true, method: "POST",
                    data: JSON.stringify({
                        limit: 12,
                        query: catalogFilter.getQuery()
                    })
                })
            }
		}
	})

})(jQuery);
