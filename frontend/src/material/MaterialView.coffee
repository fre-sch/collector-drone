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
inventory = require './inventory'
tracking = require "./tracking"


### MaterialView ###
module.exports = Backbone.View.extend
    template: _.template $("#material-tpl").html()

    className: ->
        rarity = @model.get("rarity").replace(/\W+/, "-")
        "col-sm-6 material rarity-#{rarity}"

    events:
        "click .btn.inventory-minus": "inventoryMinus"
        "click .btn.inventory-plus": "inventoryPlus"
        "click .btn.track": "track"

    initialize: (options) ->
        @inventoryItem = (inventory.get(@model.id) or
            inventory.create(id: @model.id, quantity: 0))
        @listenTo @inventoryItem, "change", @render
        @listenTo @model, "change", @render
        @listenTo @model, "destroy", @remove
        this

    render: ->
        data = @model.toJSON()
        data.inventory = if @inventoryItem then @inventoryItem.get("quantity") else 0
        @$el.html @template(data)
        this

    inventoryPlus: ->
        @inventoryItem.quantityPlus 1
        event.preventDefault()
        this

    inventoryMinus: ->
        @inventoryItem.quantityPlus -1
        event.preventDefault()
        this

    track: ->
        tracking.trackMaterial @model
        event.preventDefault()
        this
