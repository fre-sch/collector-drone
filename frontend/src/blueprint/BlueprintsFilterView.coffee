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
MenuModel = require './MenuModel'
MenuView = require './MenuView'


### BlueprintsFilterView ###
module.exports = Backbone.View.extend
    el: $("#blueprints-filter")

    events:
        "change .blueprints-filter-search": "updateSearch"

    initialize: ->
        @$searchInput = @$el.find("input.blueprints-filter-search")
        @levelMenuModel = new MenuModel
        @typeMenuModel = new MenuModel
        new MenuView
            el: @$el.find(".blueprints-filter-type")
            model: @typeMenuModel
        new MenuView
            el: @$el.find(".blueprints-filter-level")
            model: @levelMenuModel

        @listenTo @typeMenuModel, "change:selected", @updateSearch
        @listenTo @levelMenuModel, "change:selected", @updateSearch
        return this

    updateSearch: ->
        @model.set search: @$searchInput.val()
        @model.set type: @typeMenuModel.get("selected")?.value
        @model.set level: @levelMenuModel.get("selected")?.value
        return this
