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
tracking = require "./tracking"
TrackBlueprintView = require './TrackBlueprintView'
TrackMaterialView = require './TrackMaterialView'
TrackingTabView = require './TrackingTabView'


### AppView ###
module.exports = Backbone.View.extend
    el: 'body'
    events: {}
    initialize: (options) ->
        {@blueprints, @materials} = options
        @$trackMaterials = $("#track-materials")
        @$trackBlueprints = $("#track-blueprints")

        @listenTo tracking.blueprints, "add", @addTrackBlueprint
        @listenTo tracking.materials, "add", @addTrackMaterial
        @listenTo tracking.blueprints, "remove", @removeTrackBlueprint
        @listenTo tracking.materials, "remove", @removeTrackMaterial
        @listenTo tracking.blueprints, "reset", @onTrackBlueprintsReset
        @listenTo tracking.materials, "reset", @onTrackMaterialsReset

        new TrackingTabView(model: tracking)
        return this

    removeTrackMaterial: ->
        if not tracking.materials.length and not tracking.blueprints.length
            $("#introduction").show()

    removeTrackBlueprint: ->
        if not tracking.materials.length and not tracking.blueprints.length
            $("#introduction").show()

    onTrackBlueprintsReset: (collection, options) ->
        for model in collection.models
            @addTrackBlueprint(model)
        return this

    onTrackMaterialsReset: (collection, options) ->
        for model in collection.models
            @addTrackMaterial(model)
        return this

    addTrackMaterial: (trackMaterial) ->
        createViewAndAppend = _.bind((trackMaterial, material) ->
            view = new TrackMaterialView
                model: trackMaterial
                material: material
                inventory: inventory.getOrCreate(trackMaterial.id)
            $("#introduction").hide()
            @$trackMaterials.append(view.render().el)
            return
        , this, trackMaterial)

        @materials.getOrFetch trackMaterial.id,
            success: createViewAndAppend

        return this

    addTrackBlueprint: (trackBlueprint) ->
        createViewAndAppend = _.bind((trackBlueprint, blueprint) ->
            view = new TrackBlueprintView
                model:
                    trackBlueprint: trackBlueprint
                    blueprint: blueprint
            $("#introduction").hide()
            @$trackBlueprints.append view.render().el
            return this
        , this, trackBlueprint)

        @blueprints.getOrFetch trackBlueprint.id,
            success: createViewAndAppend

        return this
