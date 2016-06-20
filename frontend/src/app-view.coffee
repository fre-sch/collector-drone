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
global = exports ? this
app = global.app = global.app or {}
$ = global.jQuery


TrackingFilter = Backbone.Model.extend
  defaults:
    numBlueprints: 0
    numMaterials: 0
  initialize: (options) ->
    @listenTo app.tracking, "add remove reset", @updateQuantities
  updateQuantities: ->
    @set "numBlueprints", app.tracking.length
  plus: (attribute, value) ->
    t = @get attribute
    @set attribute, t + value

app.trackingFilter = new TrackingFilter


TrackTabView = Backbone.View.extend
  el: "#track-tab-view"
  events:
    "click a": "showTab"
  initialize: ->
    @$numBlueprints = @$el.find(".numBlueprints")
    @$numMaterials = @$el.find(".numMaterials")
    @listenTo app.trackingFilter, "change", @updateQuantities
  showTab: (event) ->
    $target = $(event.target)
    @$el.find(a).each ->
      $($(this).data("tab")).hide
    @$el.children("li").removeClass "active"
    $($target.data "tab").show
    $target.parent().addClass "active"
  updateQuantities: ->
    @$numBlueprints.html app.trackingFilter.get "numMaterials"
    @$numMaterials.html app.trackingFilter.get "numBlueprints"

app.trackTabView = new trackTabView


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

    @listenTo app.catalogFilter, "change:search change:type", @catalogFilterChanged
    @listenTo app.blueprints, "reset", @onBlueprintsReset
    @listenTo app.materials, "reset", @onMaterialsReset
    @listenTo app.tracking, "add", @addTrackingView
    @listenTo app.tracking, "reset", @onTrackingReset

    app.blueprints.fetchTypes()
      .done (blueprintTypes) ->
        for item in blueprintTypes.items
          app.catalogFilterView.addFilterItem(item)
    app.blueprints.load()
    app.materials.load()
    app.inventory.fetch(reset: true)
    app.tracking.fetch(reset: true)

  onBlueprintsReset: (collection, options) ->
    @catalogs.blueprints.empty()
    collection.each @createBlueprintView, this

  onMaterialsReset: (collection, options) ->
    @catalogs.materials.empty()
    collection.each @createMaterialView, this

  onTrackingReset: (collection, options) ->
    collection.each @addTrackingView, this

  createBlueprintView: (blueprint) ->
    view = new app.BlueprintView(model: blueprint)
    el = view.render().el
    @catalogs.blueprints.append el

  createMaterialView: (material) ->
    view = new app.MaterialView(model: material)
    el = view.render().el
    @catalogs.materials.append el

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

  addTrackingview: (trackBlueprint) ->
    createViewAndAppend = _.bind((trackBlueprint, blueprint) ->
      @addTrackBlueprintView trackBlueprint, blueprint
      for ingredient in blueprint.get "ingredients"
        @addOneTrackMaterial trackBlueprint, ingredient
    , this, trackBlueprint)
    app.blueprint.getOrFetch trackBlueprint.id,
      success: createViewAndAppend

  addTrackBlueprintView: (trackBlueprint, blueprint) ->
    view = new app.TrackBlueprintView
      model:
        trackBlueprint: TrackBlueprint
        blueprint: blueprint
    @$trackBlueprints.append view.render().el

  catalogFilterChanged: (catalogFilter, options) ->
    if catalogFilter.get("category") == "blueprints"
      console.info "catalogFilterChanged", catalogFilter.attributes
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
