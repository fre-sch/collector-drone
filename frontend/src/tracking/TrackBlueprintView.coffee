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
inventory = require './inventory'
tracking = require './tracking'


### TrackBlueprintview ###
module.exports = Backbone.View.extend
    template: _.template $("#track-blueprint-tpl").html()
    className: "col-sm-6 track-blueprint"

    events:
        "click .track": "track"
        "click .remove": "untrack"
        "click .craft": "craft"

    itemTpl: _.template("""
        <div class="row <%=itemClass%>" style="font-size: 0.9em">
          <div class="col-xs-10"><%= title %></div>
          <div class="col-xs-2 text-right">
            <span class="inventory"><%= inventory %></span>
            / <small class="quantity"><%= quantity %></small>
          </div>
        </div>""")

    initialize: (options) ->
        for ingredient in @model.blueprint.get("ingredients")
            inventoryItem = inventory.getOrCreate(ingredient.material.id)
            @listenTo inventoryItem, "change", @update
        @listenTo @model.trackBlueprint, 'change', @update
        @listenTo @model.trackBlueprint, 'destroy', @remove
        return this

    render: ->
        data = _.extend(
            @model.trackBlueprint.toJSON(),
            @model.blueprint.toJSON()
        )
        $html = $(@template(data))
        for ingredient in data.ingredients
            quantity = ingredient.quantity * @model.trackBlueprint.get("quantity")
            inventoryQuantity = inventory.get(ingredient.material.id).get("quantity")
            textClass = "text-danger" if quantity > inventoryQuantity
            itemView = @itemTpl
                itemClass: "ingredient-#{ingredient.material.id} #{textClass}"
                title: ingredient.material.title
                quantity: quantity
                inventory: inventoryQuantity

            $html.find(".ingredients").append(itemView)

        @$el.html $html
        return this

    update: ->
        @$el.find("span.blueprint-quantity").html @model.trackBlueprint.get("quantity")

        for ingredient in @model.blueprint.get("ingredients")
            quantity = ingredient.quantity * @model.trackBlueprint.get("quantity")
            inventoryQuantity = inventory.get(ingredient.material.id).get("quantity")

            if quantity > inventoryQuantity
                @$el.find(".ingredient-#{ingredient.material.id}"
                ).addClass("text-danger")
            else
                @$el.find(".ingredient-#{ingredient.material.id}"
                ).removeClass("text-danger")

            @$el.find(".ingredient-#{ingredient.material.id} .quantity"
            ).html quantity
            @$el.find(".ingredient-#{ingredient.material.id} .inventory"
            ).html inventoryQuantity

        return this

    track: ->
        tracking.trackBlueprint(@model.blueprint)

    untrack: ->
        tracking.untrackBlueprint(@model.blueprint)

    craft: ->
        @model.trackBlueprint.quantityPlus -1

        for ingredient in @model.blueprint.get("ingredients")
            inventoryItem = inventory.get(ingredient.material.id)
            amount = Math.min(ingredient.quantity, inventoryItem.get("quantity"))
            inventoryItem.quantityPlus(-amount)
            tracking.untrackMaterial(ingredient.material, ingredient.quantity)

        if @model.trackBlueprint.get("quantity") <= 0
            @untrack()
