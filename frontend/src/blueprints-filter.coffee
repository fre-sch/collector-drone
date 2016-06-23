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


BlueprintsFilter = Backbone.Model.extend
  defaults:
    type: ""
    level: null
    search: ""

  loadTypes: ->
    $.ajax
      url: "/blueprints/types"
      method: "GET"

  loadLevels: ->
    $.when [1, 2, 3, 4, 5]

  where: ->
    (model) =>
      type = model.get("type")
      level = model.get("level")
      title = model.get("title")?.toLowerCase()
      (if @get("type") then @get("type") == type else true
      ) and (if @get("level") then @get("level") == level else true
      ) and (if @get("search") then title.indexOf(@get("search").toLowerCase()) >= 0 else true)

app.blueprintsFilter = new BlueprintsFilter


BlueprintsFilterView = Backbone.View.extend
  el: $("#blueprints-filter")

  typeItemTpl: _.template(
    '<li><a href="#" data-type="<%=type%>"><%=type%></a></li>'
  )

  levelItemTpl: _.template(
    '<li><a href="#" data-level="<%=level%>">Level <%=level%></a></li>'
  )

  events:
    "change .blueprints-filter-search": "updateSearch"
    "click .blueprints-filter-type li a": "updateType"
    "click .blueprints-filter-level li a": "updateLevel"

  initialize: ->
    @$searchInput = @$el.find("input.blueprints-filter-search")
    @$typeBtn = @$el.find("span.blueprints-filter-type")
    @$typeMenu = @$el.find("ul.blueprints-filter-type")
    @$levelBtn = @$el.find("span.blueprints-filter-level")
    @$levelMenu = @$el.find("ul.blueprints-filter-level")
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

  updateLevel: ->
    $target = $(event.target)
    level = $target.data "level"
    label = $target.html()
    @$levelBtn.data "level", level
    @$levelBtn.html label
    @model.set level: level
    event.preventDefault()
    return this

  setTypes: (types) ->
    for type in types
      item = @typeItemTpl(type: type)
      @$typeMenu.append item
    @delegateEvents()
    return this

  setLevels: (levels) ->
    for level in levels
      item = @levelItemTpl(level: level)
      @$levelMenu.append item
    @delegateEvents()
    return this


app.blueprintsFilterView = new BlueprintsFilterView
  model: app.blueprintsFilter
