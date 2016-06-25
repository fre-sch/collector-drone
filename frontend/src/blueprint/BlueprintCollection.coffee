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
BlueprintModel = require "./BlueprintModel"


### BlueprintCollection ###
module.exports = Backbone.Collection.extend
    model: BlueprintModel

    url: "/blueprints"

    total: 0

    parse: (data) ->
        @total = data.count
        data.items

    getOrFetch: (id, options) ->
        mdl = @get(id)
        if mdl
            options.success mdl
        else
            @add(id: id).fetch options
