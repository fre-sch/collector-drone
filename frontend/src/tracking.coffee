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


TrackBlueprint = Backbone.Model.extend
  defaults:
    id: null
    quantity: 0
  quantityPlus: (value) ->
    q = @get "quantity"
    @save(quantity: q + value)


app.TrackMaterialView = Backbone.View.extend
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


app.TrackBlueprintView = Backbone.View.extend
  template: _.template $("#track-blueprint-tpl").html()

  className: "col-md-6 track-blueprint"

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

  initialize: ->
    for ingredient in @model.blueprint.get("ingredients")
      inventory = app.inventory.getOrCreate(ingredient.material.id)
      @listenTo inventory, "change", @update
    @listenTo @model.trackBlueprint, 'change', @update
    @listenTo @model.trackBlueprint, 'destroy', @remove
    return this

  render: ->
    data = _.extend(
      @model.trackBlueprint.toJSON(),
      @model.blueprint.toJSON()
    )
    data.tracked = true
    $html = $(@template(data))
    for ingredient in data.ingredients
      itemView = @itemTpl
        itemClass: "ingredient-#{ingredient.material.id}"
        title: ingredient.material.title
        quantity: ingredient.quantity * @model.trackBlueprint.get("quantity")
        inventory: app.inventory.get(ingredient.material.id).get("quantity")

      $html.find(".ingredients").append(itemView)

    @$el.html $html
    return this

  update: ->
    @$el.find("span.blueprint-quantity").html @model.trackBlueprint.get("quantity")

    for ingredient in @model.blueprint.get("ingredients")
      quantity = ingredient.quantity * @model.trackBlueprint.get("quantity")
      inventory = app.inventory.get(ingredient.material.id).get("quantity")
      @$el.find(".ingredient-#{ingredient.material.id} .quantity"
      ).html quantity
      @$el.find(".ingredient-#{ingredient.material.id} .inventory"
      ).html inventory

    return this

  track: ->
    @model.trackBlueprint.quantityPlus 1

  untrack: ->
    @model.trackBlueprint.destroy()

  craft: ->
    @model.trackBlueprint.quantityPlus -1
    if @model.trackBlueprint.get("quantity") <= 0
      @untrack()


TrackingCollection = Backbone.Collection.extend
  model: TrackBlueprint
  localStorage: new Backbone.LocalStorage "trackBlueprint"

app.tracking = new TrackingCollection
