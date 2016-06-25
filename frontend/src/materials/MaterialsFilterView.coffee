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


### MaterialsFilterView ###
module.exports = Backbone.View.extend
    events:
        "change .materials-filter-search": "updateSearch"

    initialize: ->
        @$searchInput = @$el.find("input.materials-filter-search")
        @typeMenuModel = new MenuModel
        @sortMenuModel = new MenuModel

        new MenuView
            el: @$el.find(".materials-sort")
            model: @sortMenuModel

        new MenuView
            el: @$el.find(".materials-filter-type")
            model: @typeMenuModel

        @sortMenuModel.set items: [
            {label: "Title", value: "title"}
            {label: "Type", value: "type"}
            {label: "Rarity", value: "rarity"}
            {label: "Inventory", value: "inventory"}
        ]

        @listenTo @typeMenuModel, "change:selected", @updateFilterModel
        @listenTo @sortMenuModel, "change:selected", @updateFilterModel
        return this

    updateFilterModel: ->
        @model.set search: @$searchInput.val()
        @model.set type: @typeMenuModel.get("selected")?.value
        @model.set sort: @sortMenuModel.get("selected")?.value
        return this
