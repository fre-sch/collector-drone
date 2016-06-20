/*
Companion web-app for Elite: Dangerous, manage blueprints and material inventory
for crafting engineer upgrades.
Copyright (C) 2016  Frederik Schumacher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
/*global Backbone, jQuery, _, ENTER_KEY, ESC_KEY */
var app = app || {};

(function($) {
  'use strict';

  app.MaterialView = Backbone.View.extend({
    template: _.template($('#material-tpl').html()),
    className: "col-md-4 material",
    events: {
      "click a.inventory-minus": "inventoryMinus",
      "click a.inventory-plus": "inventoryPlus"
    },
    initialize: function() {
      this.inventory = (
        app.inventory.get(this.model.id) ||
        app.inventory.create({
          id: this.model.id,
          quantity: 0
        })
      )
      this.listenTo(this.inventory, "change", this.render)
      this.listenTo(this.model, 'change', this.render)
      this.listenTo(this.model, 'destroy', this.remove)
    },
    render: function() {
      var data = this.model.toJSON()
      data.inventory = this.inventory ? this.inventory.get("quantity") : 0
      this.$el.html(this.template(data))
      return this
    },
    inventoryPlus: function() {
      this.inventory.quantityPlus(1)
    },
    inventoryMinus: function() {
      this.inventory.quantityPlus(-1)
    }
  });
})(jQuery);
