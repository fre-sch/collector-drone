/*global Backbone, jQuery, _, ENTER_KEY, ESC_KEY */
var app = app || {};

(function ($) {
	'use strict'

    var CatalogFilterModel = Backbone.Model.extend({
        defaults: {
            category: "blueprints",
            type: "",
            search: ""
        },
        getFilter: function() {
            if (this.get("category") == "blueprints")
                return this.get("blueprintsFilter")
            else if (this.get("category") == "materials")
                return this.get("materialsFilter")
        },
	    getQuery: function() {
	        var query = {and: []}
	        var filter = this.getFilter()
            if (filter.search) {
                query.and.push({ilike: {
                    title: "%" + fiter.search + "%"
                }})
            }
            if (filter.type) {
                query.and.push({eq: {type: filter.type}})
            }
            return query
	    }
    })
    app.catalogFilter = new CatalogFilterModel()


	var CatalogFilterView = Backbone.View.extend({
	    el: "#resources-toolbar",
	    dropdownItemTpl: _.template(
	        '<li><a href="#" data-type="<%=type%>"><%=title%></a></li>'
        ),
	    events: {
	        "click #catalog-filter-category a": "setCategory",
	        "change #catalog-filter-search": "setSearch",
	        "keypress #catalog-filter-search": "setSearchOnEnter",
	        "click #catalog-filter-types a": "setType"
	    },
	    initialize: function() {
	        this.$dropdown = $("#catalog-filter-types")
	        this.$searchInput = $("#catalog-filter-search")
	        this.catalogs = {
	            blueprints: $("#catalog-blueprints"),
	            materials: $("#catalog-materials"),
	            engineers: $("#catalog-engineers")
	        }
	        this.listenTo(app.blueprints, "reset", this.update)
	        this.listenTo(app.materials, "reset", this.update)
	    },
	    addFilterItem: function(item) {
            this.$dropdown.append(this.dropdownItemTpl({
                type: item, title: item
            }))
            return this
	    },
	    setType: function() {
	        var $target = $(event.target)
	        $("#catalog-filter-type-sel").html($target.html())
	        this.model.set("type", $target.data("type"))
	    },
	    setCategory: function() {
	        var $target = $(event.target)
	        var category = $target.data("category")
            $target.parent()
                .addClass("active")
                .siblings()
                .removeClass("active")
            this.catalogs[category].show().siblings().hide()
	        this.model.set("category", category)
	    },
	    setSearchOnEnter: function(e) {
            if (e.which === ENTER_KEY) {
                this.setSearch()
            }
	    },
	    setSearch: function() {
	        var value = this.$searchInput.val()
	        this.model.set({search: value})
	    },
	    update: function() {
	        this.$el.find("#num-blueprints").html(
	            app.blueprints.total)
	        this.$el.find("#num-materials").html(
	            app.materials.total)
	    }
	})
	app.catalogFilterView = new CatalogFilterView({model: app.catalogFilter})

})(jQuery);
