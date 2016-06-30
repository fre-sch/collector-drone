###
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
###

AppView = require "./AppView"
FilteredCollection = require "./FilteredCollection"
PagerModel = require "./PagerModel"
BlueprintCollection = require "./BlueprintCollection"
BlueprintsCollectionView = require "./BlueprintsCollectionView"
BlueprintsFilter = require "./BlueprintsFilter"
BlueprintsFilterView = require './BlueprintsFilterView'
MaterialCollection = require "./MaterialCollection"
MaterialsCollectionView = require './MaterialsCollectionView'
MaterialsFilter = require "./MaterialsFilter"
MaterialsFilterView = require "./MaterialsFilterView"
ResourceTabView = require "./ResourceTabView"
tracking = require './tracking'
inventory = require './inventory'


### App.js ###
App = ->
    $.ajaxSetup(contentType: "application/json")

    blueprintsFilter = new BlueprintsFilter
    blueprintsFiltered = FilteredCollection(
        new BlueprintCollection, blueprintsFilter)

    materialsFilter = new MaterialsFilter
    materialsFiltered = FilteredCollection(
        new MaterialCollection, materialsFilter)

    @blueprintsCollectionView = new BlueprintsCollectionView
        model: blueprintsFiltered
        pager: new PagerModel(collection: blueprintsFiltered)

    @materialsCollectionView = new MaterialsCollectionView
        model: materialsFiltered
        pager: new PagerModel(collection: materialsFiltered)

    blueprintsFilterView = new BlueprintsFilterView
        model: blueprintsFilter

    materialsFilterView = new MaterialsFilterView
        el: $("#materials-filter")
        model: materialsFilter

    materialsFilterView.typeMenuModel.set
        items: CollectorDroneData.materialTypes

    blueprintsFilterView.typeMenuModel.set
        items: CollectorDroneData.blueprintTypes

    blueprintsFilterView.levelMenuModel.set items:
        for item in blueprintsFilter.loadLevels()
            label: item, value: item

    @resourceTabView = new ResourceTabView
        blueprintsCollection: blueprintsFiltered
        materialsCollection: materialsFiltered

    @view = new AppView
        blueprints: blueprintsFiltered
        materials: materialsFiltered

    inventory.fetch(reset: true)
    blueprintsFiltered._source.reset(CollectorDroneData.blueprints)
    materialsFiltered._source.reset(CollectorDroneData.materials)
    tracking.materials.fetch(reset: true)
    tracking.blueprints.fetch(reset: true)
    return this

new App()
