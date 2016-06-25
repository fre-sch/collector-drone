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


### App.js ###
App = ->
    "use strict"

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

    @blueprintsFilterView = new BlueprintsFilterView
        model: blueprintsFilter

    @materialsCollectionView = new MaterialsCollectionView
        model: materialsFiltered
        pager: new PagerModel(collection: materialsFiltered)

    @materialsFilterView = new MaterialsFilterView
        model: materialsFilter

    @resourceTabView = new ResourceTabView
        blueprintsCollection: blueprintsFiltered
        materialsCollection: materialsFiltered

    @view = new AppView
        blueprints: blueprintsFiltered
        materials: materialsFiltered
        blueprintsFilter: blueprintsFilter
        blueprintsFilterView: @blueprintsFilterView
        materialsFilter: materialsFilter
        materialsFilterView: @materialsFilterView

    return this

new App()
