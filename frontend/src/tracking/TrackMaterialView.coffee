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


### TrackMaterialView ###
module.exports = Backbone.View.extend
    template: _.template $("#track-material-tpl").html()

    className: "col-md-4"

    events:
        "click .inventory-plus": "inventoryPlus"
        "click .inventory-minus": "inventoryMinus"

    initialize: (options) ->
        @listenTo @model.inventory, 'change', @update
        @listenTo @model.trackBlueprint, "change", @update
        @listenTo @model.trackBlueprint, 'destroy', @remove

    render: ->
        data =
            quantity: @model.trackBlueprint.get("quantity") * @model.ingredient.quantity
            inventory: @model.inventory.get("quantity")
            material: @model.material.toJSON()
        @$el.html @template(data)
        return this

    update: ->
        @$el.find("span.inventory").html(@model.inventory.get("quantity"))
        @$el.find("span.quantity").html(
            @model.trackBlueprint.get("quantity") * @model.ingredient.quantity
        )

    inventoryPlus: ->
        @model.inventory.quantityPlus 1

    inventoryMinus: ->
        @model.inventory.quantityPlus -1
