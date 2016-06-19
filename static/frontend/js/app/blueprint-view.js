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

(function ($) {
	'use strict';

	app.BlueprintView = Backbone.View.extend({
		template: _.template($('#blueprint-tpl').html()),
		className: "col-md-6 blueprint",

		events: {
            "click a.bookmark": "bookmark",
            "click a.track": "track",
		},

		initialize: function () {
			this.listenTo(this.model, 'change', this.render);
			this.listenTo(this.model, 'destroy', this.remove);
		},

		render: function () {
			this.$el.html(this.template(this.model.toJSON()))
			return this
		},

		bookmark: function() {
		    alert("not implemented")
		},

		track: function() {
		    var that = this
		    var trackedBlueprint = app.tracking.get(this.model.id)
		    if (!trackedBlueprint) {
		        app.tracking.create({
		            id: this.model.id,
		            quantity: 1
		        })
		    }
		    else {
		        trackedBlueprint.quantityPlus(1)
		    }
		}
	});
})(jQuery);
