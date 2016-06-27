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


### MenuView ###
module.exports = Backbone.View.extend
    itemTemplate: _.template(
        '<li><a href="#" data-value="<%=value%>"><%=label%></a></li>')

    events:
        "click .dropdown-menu li a": "itemClicked"

    initialize: ->
        @$button = @$el.find(".btn-group .btn-label")
        @$menu = @$el.find(".btn-group .dropdown-menu")
        @listenTo @model, "change:items", @updateMenuItems
        @listenTo @model, "change:selected", @updateButton

    updateMenuItems: ->
        @$menu.find(".divider").nextAll().remove()
        for item in @model.get "items"
            @$menu.append @itemTemplate(item)
        @delegateEvents()

    updateButton: ->
        item = @model.get "selected"
        @$button.html item.label

    itemClicked: ->
        $target = $(event.target)
        item =
            value: $target.data "value"
            label: $target.html()
        @model.set selected: item
        event.preventDefault()
        return this
