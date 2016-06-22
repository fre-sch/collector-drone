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


ResourceTabView = Backbone.View.extend
  el: "#resource-filter-tabs"

  initialize: (options) ->
    @$badgeNumBlueprints = @$el.find "span.num-blueprints"
    @$badgeNumMaterials = @$el.find "span.num-materials"
    @listenTo app.blueprints, "reset", @update
    @listenTo app.materials, "reset", @update
    this

  update: ->
    @$badgeNumBlueprints.html app.blueprints.total
    @$badgeNumMaterials.html app.materials.total
    this

app.resourceTabView = new ResourceTabView
