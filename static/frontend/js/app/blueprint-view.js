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
