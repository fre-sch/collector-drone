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


### PagerView ###
module.exports = Backbone.View.extend
    events:
        "click .previous": "previous"
        "click .next": "next"
        "click .page": "goto"

    itemTpl: _.template("""<a href="#"
            data-page="<%=page%>"
            class="page page-<%=page%><%=(active?" active":"")%>"><%=page%></a>""")

    initialize: ->
        @listenTo @model, "change:pages", @pagesChanged
        @listenTo @model, "change:current", @currentChanged

    pagesChanged: ->
        @$el.find(".page").remove()
        numPages = @model.get("pages")
        items = []
        items.push @itemTpl(active: i == 1, page: i) for i in [1..numPages]
        @$el.find(".drone-pages").html(items.join "")
        @delegateEvents()

    currentChanged: ->
        current = @model.get("current")
        @$el.find(".page-#{current}")
            .addClass("active")
            .siblings().removeClass("active")
        return this

    next: (event)->
        @model.next()
        event.preventDefault()

    previous: (event)->
        @model.previous()
        event.preventDefault()

    goto: (event)->
        @model.set current: $(event.target).data("page")
        event.preventDefault()
