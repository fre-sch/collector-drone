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


### Ga ###
class Ga
    constructor: (model)->
        model.on "action:blueprint:track", @sendBlueprintTrack
        model.on "action:blueprint:untrack", @sendBlueprintUntrack
        model.on "action:blueprint:craft", @sendBlueprintCraft
        model.on "action:inventory:plus", @sendInventoryPlus
        model.on "action:inventory:minus", @sendInventoryMinus
        model.on "action:blueprint:filter", @sendBlueprintFilter
        model.on "action:material:filter", @sendMaterialFilter

    sendBlueprintTrack: ()->
        window.ga "send", "event",
            eventCategory: "blueprint"
            eventAction: "track"
            eventLabel: "Track blueprint"

    sendBlueprintUntrack: ()->
        window.ga "send", "event",
            eventCategory: "blueprint"
            eventAction: "untrack"
            eventLabel: "Untrack blueprint"

    sendBlueprintCraft: ()->
        window.ga "send", "event",
            eventCategory: "blueprint"
            eventAction: "craft"
            eventLabel: "Craft blueprint"

    sendInventoryPlus: ()->
        window.ga "send", "event",
            eventCategory: "inventory"
            eventAction: "plus"
            eventLabel: "Increase material inventory"

    sendInventoryMinus: ()->
        window.ga "send", "event",
            eventCategory: "inventory"
            eventAction: "minus"
            eventLabel: "Decrease material inventory"

    sendBlueprintFilter: ()->
        window.ga "send", "event",
            eventCategory: "blueprint"
            eventAction: "filter"
            eventLabel: "Filter/search blueprints"

    sendMaterialFilter: ()->
        window.ga "send", "event",
            eventCategory: "material"
            eventAction: "filter"
            eventLabel: "Filter/search material"


module.exports = Ga
