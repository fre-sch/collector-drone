# Unofficial companion web-app for Elite: Dangerous (property of Frontier
# Developments). Collector-Drone lets you manage blueprints and material
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
MenuModel = require './MenuModel'
MenuView = require './MenuView'


### BlueprintsFilterView ###
module.exports = Backbone.View.extend
    el: $("#blueprints-filter")

    events:
        "change .blueprints-filter-search": "updateFilterModel"

    initialize: ->
        @$searchInput = @$el.find("input.blueprints-filter-search")
        @levelMenuModel = new MenuModel
        @typeMenuModel = new MenuModel
        @sortMenuModel = new MenuModel

        new MenuView
            el: @$el.find(".blueprints-filter-type")
            model: @typeMenuModel
        new MenuView
            el: @$el.find(".blueprints-filter-level")
            model: @levelMenuModel
        new MenuView
            el: @$el.find(".blueprints-sort")
            model: @sortMenuModel

        @sortMenuModel.set items: [
            {label: "Title A-Z", value: "title,asc"}
            {label: "Title Z-A", value: "title,desc"}
            {label: "Type A-Z", value: "type,asc"}
            {label: "Type Z-A", value: "type,desc"}
            {label: "Level 0-9", value: "level,asc"}
            {label: "Level 9-0", value: "level,desc"}
        ]

        @listenTo @typeMenuModel, "change:selected", @updateFilterModel
        @listenTo @levelMenuModel, "change:selected", @updateFilterModel
        @listenTo @sortMenuModel, "change:selected", @updateFilterModel
        return this

    updateFilterModel: ->
        @model.set search: @$searchInput.val()
        @model.set type: @typeMenuModel.get("selected")?.value
        @model.set level: @levelMenuModel.get("selected")?.value
        @model.set sort: @sortMenuModel.get("selected")?.value
        return this
