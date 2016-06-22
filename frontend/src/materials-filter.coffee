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


MaterialsFilter = Backbone.Model.extend
  defaults:
    category: "blueprints"
    type: ""
    search: ""

  loadTypes: ->
    $.ajax
      url: "/materials/types"
      method: "GET"

  getQuery: ->
    query = and: []
    if @get "search"
      query.and.push(ilike: title: "%#{@get "search"}%")
    if @get "type"
      query.and.push(eq: type: @get "type")
    query

app.materialsFilter = new MaterialsFilter


MaterialsFilterView = Backbone.View.extend
  el: $("#materials-filter")

  typeItemTpl: _.template(
    '<li><a href="#" data-type="<%=type%>"><%=type%></a></li>'
  )

  events:
    "change .materials-filter-search": "updateSearch"
    "click .materials-filter-type li a": "updateType"

  initialize: ->
    @$searchInput = @$el.find("input.materials-filter-search")
    @$typeBtn = @$el.find("span.materials-filter-type")
    @$typeMenu = @$el.find("ul.materials-filter-type")
    return this

  updateSearch: ->
    @model.set search: @$searchInput.val()
    return this

  updateType: ->
    $target = $(event.target)
    type = $target.data "type"
    label = $target.html()
    @$typeBtn.data "type", type
    @$typeBtn.html label
    @model.set type: type
    event.preventDefault()
    return this

  setTypes: (types) ->
    for type in types when type
      item = @typeItemTpl(type: type)
      @$typeMenu.append item
    @delegateEvents()
    return this


app.materialsFilterView = new MaterialsFilterView
  model: app.materialsFilter
