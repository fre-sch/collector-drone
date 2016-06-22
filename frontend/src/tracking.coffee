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
    app.trackingFilter.plus("numMaterials", 1)
    @listenTo @model.inventory, 'change', @render
    @listenTo @model.trackBlueprint, "change", @render
    @listenTo @model.trackBlueprint, 'destroy', @remove
    @listenTo @model.trackBlueprint, 'destroy', @updateTrackingFilter
  render: ->
    data =
      quantity: @model.trackBlueprint.get("quantity") * @model.ingredient.quantity
      inventory: @model.inventory.get("quantity")
      material: @model.material.toJSON()
    @$el.html @template(data)
    return this
  updateTrackingFilter: ->
    app.trackingFilter.plus("numMaterials", -1)
  inventoryPlus: ->
    @model.inventory.quantityPlus 1
  inventoryMinus: ->
    @model.inventory.quantityPlus -1


app.TrackBlueprintView = Backbone.View.extend
  template: _.template $("#blueprint-tpl").html()
  className: "col-md-6"
  events:
    "click .track": "track"
    "click .remove": "untrack"
    "click .craft": "craft"
  initialize: ->
    @listenTo @model.trackBlueprint, 'change', @render
    @listenTo @model.trackBlueprint, 'destroy', @remove
  render: ->
    data = _.extend(
      @model.trackBlueprint.toJSON(),
      @model.blueprint.toJSON()
    )
    data.tracked = true
    @$el.html @template(data)
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
