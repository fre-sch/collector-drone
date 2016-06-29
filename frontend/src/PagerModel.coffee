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
        offset: 0
        collection: null

    total: ->
        @get("collection").size()

    max: ->
        Math.floor((@total() - 1) / @get("limit") ) * @get("limit")

    next: ->
        offset = Math.min(@get("offset") + @get("limit"), @max())
        @set offset: offset
        return this

    previous: ->
        offset = Math.max(@get("offset") - @get("limit"), 0)
        @set offset: offset
        return this

    pages: ->
        maxPage = @max() / @get("limit")
        for i in [1..maxPage]
            page: i
            offset: (i - 1) * @get("limit")
