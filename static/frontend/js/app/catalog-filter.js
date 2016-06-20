/*
Companion web-app for Elite: Dangerous, manage blueprints and material inventory
for crafting engineer upgrades.
Copyright (C) 2016  Frederik Schumacher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
/*global Backbone, jQuery, _, ENTER_KEY, ESC_KEY */
var app = app || {};

(function($) {
  'use strict'

  var CatalogFilterModel = Backbone.Model.extend({
    defaults: {
      category: "blueprints",
      type: "",
      search: ""
    },
    getQuery: function() {
      var query = {
        and: []
      }
      if (this.get("search")) {
        query.and.push({
          ilike: {
            title: "%" + this.get("search") + "%"
          }
        })
      }
      if (this.get("type")) {
        query.and.push({
          eq: {
            type: this.get("type")
          }
        })
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
        type: item,
        title: item
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
      this.model.set({
        search: value
      })
    },
    update: function() {
      this.$el.find("#num-blueprints").html(
        app.blueprints.total)
      this.$el.find("#num-materials").html(
        app.materials.total)
    }
  })
  app.catalogFilterView = new CatalogFilterView({
    model: app.catalogFilter
  })

})(jQuery);
