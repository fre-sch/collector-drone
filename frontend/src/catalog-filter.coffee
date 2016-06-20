# Companion web-app for Elite: Dangerous, manage blueprints and material
# inventory for crafting engineer upgrades.
# Copyright (C) 2016  Frederik Schumacher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
global = exports ? this
app = global.app = global.app or {}
$ = global.jQuery

CatalogFilterModel = Backbone.Model.extend
  defaults:
    category: "blueprints"
    type: ""
    search: ""

  getQuery: ->
    query: and: []
    if @get "search"
      query.and.push(ilike: title: "%#{@get "search"}%")
    if @get "type"
      query.and.push(eq: type: @get "type")
    query

app.catalogFilter = new CatalogFilterModel


CatalogFilterView = Backbone.View.extend
  el: "#resources-toolbar"
  dropdownItemTpl: _.template(
    '<li><a href="#" data-type="<%=type%>"><%=title%></a></li>'
  )
  events:
    "click #catalog-filter-category a": "setCategory"
    "change #catalog-filter-search": "setSearch"
    "keypress #catalog-filter-search": "setSearchOnEnter"
    "click #catalog-filter-types a": "setType"

  initialize: (options) ->
    @$dropdown = $("#catalog-filter-types")
    @$searchInput = $("#catalog-filter-search")
    @catalogs =
      blueprints: $("#catalog-blueprints")
      materials: $("#catalog-materials")
      engineers: $("#catalog-engineers")
    @listenTo app.blueprints, "reset", @update
    @listenTo app.materials, "reset", @update

  addFilterItem: (item) ->
    @$dropdown.append @dropdownItemTpl(
      type: item
      title: item
    )
    this

  setType: ->
    $target = $(event.target)
    $("#catalog-filter-type-sel").html $target.html()
    @model.set "type", $target.data("type")

  setCategory: ->
    $target = $(event.target)
    category = $target.data("category")
    $target.parent().addClass("active").siblings().removeClass("active")
    @catalogs[category].show().siblings().hide()
    @model.set "category", category

  setSearchOnEnter: (e) ->
    if e.which == global.ENTER_KEY
      @setSearch()

  setSearch: ->
    value = @$searchInput.val()
    @model.set "search", value

  update: ->
    @$el.find("#num-blueprints").html(app.blueprints.total)
    @$el.find("#num-materials").html(app.materials.total)

app.catalogFilterView = new CatalogFilterView(model: app.catalogFilter)
