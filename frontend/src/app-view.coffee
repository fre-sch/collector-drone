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


app.AppView = Backbone.View.extend
  el: 'body'
  events: {}
  initialize: (options) ->
    @catalogs =
      blueprints: $("#catalog-blueprints")
      materails: $("#catalog-materials")
      engineers: $("#catalog-engineers")
    @$trackMaterials = $("#track-materials")
    @$trackBlueprints = $("#track-blueprints")

    @listenTo app.tracking, "add", @addTrackingView
    @listenTo app.tracking, "reset", @onTrackingReset

    app.blueprintsFilter.loadTypes()
      .done (data) ->
        app.blueprintsFilterView.setTypes data.items
        null

    app.materialsFilter.loadTypes()
      .done (data) ->
        app.materialsFilterView.setTypes data.items
        null

    app.blueprintsFilter.loadLevels()
      .done (data) ->
        app.blueprintsFilterView.setLevels data
        null

    app.blueprints.load()
    app.materials.load()
    app.inventory.fetch(reset: true)
    app.tracking.fetch(reset: true)

  onTrackingReset: (collection, options) ->
    for model in collection.models
      @addTrackingView(model)
    return this

  addOneTrackMaterial: (trackBlueprint, ingredient) ->
    createViewAndAppend = _.bind((trackBlueprint, material) ->
      view = new app.TrackMaterialView
        model:
          material: material
          ingredient: ingredient
          inventory: app.inventory.getOrCreate(id: material.id)
          trackBlueprint: trackBlueprint

      @$trackMaterials.append(view.render().el)
    , this, trackBlueprint)
    app.materials.getOrFetch ingredient.material.id,
      success: createViewAndAppend
    return this

  addTrackingView: (trackBlueprint) ->
    createViewAndAppend = _.bind((trackBlueprint, blueprint) ->
      @addTrackBlueprintView trackBlueprint, blueprint
      for ingredient in blueprint.get "ingredients"
        @addOneTrackMaterial trackBlueprint, ingredient
    , this, trackBlueprint)
    app.blueprints.getOrFetch trackBlueprint.id,
      success: createViewAndAppend
    return this

  addTrackBlueprintView: (trackBlueprint, blueprint) ->
    view = new app.TrackBlueprintView
      model:
        trackBlueprint: trackBlueprint
        blueprint: blueprint
    @$trackBlueprints.append view.render().el
    return this

  catalogFilterChanged: (catalogFilter, options) ->
    if catalogFilter.get("category") == "blueprints"
      app.blueprints.fetch
        reset: true
        method: "POST"
        data: JSON.stringify
          limit: 12
          query: catalogFilter.getQuery()
    else if catalogFilter.get("category") == "materials"
      app.materials.fetch
        reset: true
        method: "POST"
        data: JSON.stringify
          limit: 12
          query: catalogFilter.getQuery()
    return this
