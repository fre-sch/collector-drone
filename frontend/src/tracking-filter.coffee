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
