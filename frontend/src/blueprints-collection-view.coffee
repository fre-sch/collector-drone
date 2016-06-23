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


BlueprintsCollectionView = Backbone.View.extend
  el: $("#blueprints-collection-view .collection-items")
  limit: 12

  initialize: (options) ->
    {@filter, @pager} = options

    new PagerView
      el: "#blueprints-collection-view .pager"
      model: @pager

    @listenTo @model, "reset", @render
    @listenTo @filter, "change", @render
    @listenTo @pager, "change", @render
    return this

  render: ->
    @$el.empty()
    models = @model.filter @filter.where()
    begin = @pager.get("offset")
    end = @pager.get("offset") + @pager.get("limit")
    @createItemView model for model, i in models.slice begin, end
    return this
    
  createItemView: (model) ->
    view = new app.BlueprintView(model: model)
    el = view.render().el
    @$el.append el
    return this


app.blueprintsCollectionView = new BlueprintsCollectionView
  model: app.blueprints
  filter: app.blueprintsFilter
  pager: new Pager(collection: app.blueprints)
