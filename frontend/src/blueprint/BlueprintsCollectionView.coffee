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
PagerView = require './PagerView'
BlueprintView = require './BlueprintView'


### BlueprintsCollectionView ###
module.exports = Backbone.View.extend
    el: $("#blueprints-collection-view .collection-items")
    limit: 12

    initialize: (options) ->
        {@filter, @pager} = options

        @filter.on "change", => @pager.set offset: 0

        new PagerView
            el: "#blueprints-collection-view .drone-pagination"
            model: @pager

        @listenTo @model, "reset", @render
        @listenTo @pager, "change", @render
        return this

    render: ->
        @$el.empty()
        begin = @pager.offset()
        end = @pager.offset() + @pager.get("limit")
        @createItemView model, i for model, i in @model.slice begin, end
        return this

    createItemView: (model, i) ->
        view = new BlueprintView(model: model)
        el = view.render().el
        @$el.append el
        return this
