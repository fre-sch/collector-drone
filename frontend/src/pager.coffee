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
# You should have received a copy of the GNU General Public L icense
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


Pager = Backbone.Model.extend
  defaults:
    limit: 12
    offset: 0
    collection: null

  total: ->
    @get("collection").total ? @get("collection").size()

  next: ->
    max = Math.floor((@total() - 1) / @get("limit") ) * @get("limit")
    offset = Math.min(@get("offset") + @get("limit"), max)
    @set offset: offset
    return this

  previous: ->
    offset = Math.max(@get("offset") - @get("limit"), 0)
    @set offset: offset
    return this


PagerView = Backbone.View.extend
  events:
    "click .previous": "previous"
    "click .next": "next"

  next: ->
    @model.next()
    event.preventDefault()

  previous: ->
    @model.previous()
    event.preventDefault()
