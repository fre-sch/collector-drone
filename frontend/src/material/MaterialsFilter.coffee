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
utils = require './utils'


### MaterialsFilter ###
module.exports = Backbone.Model.extend
    defaults:
        type: ""
        search: ""
        sort: null

    where: ->
        (model) =>
            type = model.get("type")
            title = model.get("title")?.toLowerCase()
            _.every([
                if @get("type") then @get("type") == type else true,
                if @get("search") then title.indexOf(@get("search").toLowerCase()) >= 0 else true
            ])

    sort: ->
        sort = @get "sort"
        if sort
            [field, dir] = sort.split(",")
            if field == "inventory"
                return (model) -> model.inventoryQuantity()
            else if dir == "desc"
                return (a, b) -> utils.cmp(b.get(field), a.get(field))
            else if dir == "asc"
                return (a, b) -> utils.cmp(a.get(field), b.get(field))
