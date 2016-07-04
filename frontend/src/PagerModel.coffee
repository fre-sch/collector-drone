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
# You should have received a copy of the GNU General Public L icense
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


### PagerModel ###
module.exports = Backbone.Model.extend
    defaults:
        limit: 12
        current: 1
        pages: 1
        collection: null

    initialize: ->
        @listenTo @get("collection"), "reset", @updatePages

    updatePages: ->
        @set
            current: 1
            pages: @calcPages()

    calcPages: ->
        Math.max(1, Math.ceil(@total() / @get("limit")))

    total: ->
        @get("collection").size()

    max: ->
        Math.floor((@total() - 1) / @get("limit") ) * @get("limit")

    next: ->
        @set current: Math.min(@get("current") + 1, @get("pages"))
        return this

    previous: ->
        @set current: Math.max(@get("current") - 1, 1)
        return this

    offset: ->
        offset = (@get("current") - 1) * @get("limit")
        Math.max(0, offset)
