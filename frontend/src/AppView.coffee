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
TrackBlueprintView = require './TrackBlueprintView'
TrackMaterialView = require './TrackMaterialView'
TrackingTabView = require './TrackingTabView'


### AppView ###
module.exports = Backbone.View.extend
    el: 'body'
    events: {}
    initialize: (options) ->
        {@blueprints,
        @materials,
        blueprintsFilter,
        blueprintsFilterView,
        materialsFilter,
        materialsFilterView} = options
        @$trackMaterials = $("#track-materials")
        @$trackBlueprints = $("#track-blueprints")

        @listenTo tracking, "add", @addTrackingView
        @listenTo tracking, "reset", @onTrackingReset

        blueprintsFilter.loadTypes()
            .done (data) ->
                blueprintsFilterView.setTypes data.items
                null

        materialsFilter.loadTypes()
            .done (data) ->
                materialsFilterView.setTypes data.items
                null

        blueprintsFilter.loadLevels()
            .done (data) ->
                blueprintsFilterView.setLevels data
                null

        @trackTabView = new TrackingTabView
          model: tracking

        @blueprints.fetch(reset: true)
        @materials.fetch(reset: true)
        inventory.fetch(reset: true)
        tracking.fetch(reset: true)
        this

    onTrackingReset: (collection, options) ->
        for model in collection.models
            @addTrackingView(model)
        return this

    addOneTrackMaterial: (trackBlueprint, ingredient) ->
        createViewAndAppend = _.bind((trackBlueprint, material) ->
            view = new TrackMaterialView
                model:
                    material: material
                    ingredient: ingredient
                    inventory: inventory.getOrCreate(material.id)
                    trackBlueprint: trackBlueprint

            @$trackMaterials.append(view.render().el)
        , this, trackBlueprint)
        @materials.getOrFetch ingredient.material.id,
            success: createViewAndAppend
        return this

    addTrackingView: (trackBlueprint) ->
        createViewAndAppend = _.bind((trackBlueprint, blueprint) ->
            @addTrackBlueprintView trackBlueprint, blueprint
            for ingredient in blueprint.get "ingredients"
                @addOneTrackMaterial trackBlueprint, ingredient
        , this, trackBlueprint)
        @blueprints.getOrFetch trackBlueprint.id,
            success: createViewAndAppend
        return this

    addTrackBlueprintView: (trackBlueprint, blueprint) ->
        view = new TrackBlueprintView
            model:
                trackBlueprint: trackBlueprint
                blueprint: blueprint

        @$trackBlueprints.append view.render().el
        return this
