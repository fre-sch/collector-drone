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


PagerView = Backbone.View.extend
  events:
    "click .previous": "previous"
    "click .next": "next"
  
  # pageTpl: _.template('<li class="page"><a href="#" data-offset="<%=offset%>"><%=page%></a></li>')
  #
  # initialize: ->
  #   @$at = @$el.find(".next")
  #   @listenTo @model, "change", @render
  #   @listenTo @model.get("collection"), "reset", @render
  #   return this
  #
  # render: ->
  #   @$el.find(".page").remove()
  #   for page in @model.pages()
  #     @$at.before @pageTpl(page)
  #   return this

  next: ->
    @model.next()
    event.preventDefault()

  previous: ->
    @model.previous()
    event.preventDefault()
