/*global Backbone, jQuery, _, ENTER_KEY, ESC_KEY */
var app = app || {};

(function ($) {
	'use strict';

	app.MaterialView = Backbone.View.extend({
		template: _.template($('#material-tpl').html()),
		className: "col-md-4 material",
		events: {
		},
		initialize: function () {
		    this.inventory = app.inventory.get(this.model.id)
		    this.listenTo(this.inventory, "change", this.render)
			this.listenTo(this.model, 'change', this.render)
			this.listenTo(this.model, 'destroy', this.remove)
		},
		render: function () {
		    var data = this.model.toJSON()
		    data.inventory = this.inventory ? this.inventory.get("quantity") : 0
			this.$el.html(this.template(data))
			return this
		}
	});
})(jQuery);
