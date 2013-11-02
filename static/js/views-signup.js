
$.validator.addMethod('username', function(value, element) {
	return this.optional(element) || /^[a-z0-9]{2,}$/i.test(value);
}, 'Please enter an alphanumeric user name of 2 or more characters.');


var SignupView = Backbone.View.extend({
	el: '#middle',
	events: {
		'click #go': 'go'
	},
	initialize: function(opts) {
		_.bindAll(this, 'go', 'submit');
        this.config = opts.config;
		this.$('form').validate({
			rules: {
				username: { required: true, username: true },
				fullname: { required: true },
				email: { email: true },
				password: { minlength: 8 },
				password2: { equalTo: '#password' }
			}
		});
	},
	go: function() {
		var that = this;
		if (this.$('form').valid()) {
			this.submit(function(status) {
				switch(status) {
				case 'success':
					var templFunc = _.template($('#success-template').html());
					that.$el.html(templFunc());
					break;
				case 'taken':
					this.$('.username-taken').slideDown(200);
					break;
				default:
					alert('Sorry!  We are ran into a problem trying to ' +
						'sign you up.');
					break;
				}
			});
		}
	},
	submit: function(cb) {
		var data = {
			username: this.$('#username').val(),
			fullname: this.$('#fullname').val().trim(),
			email: this.$('#email').val(),
			password: this.$('#password').val()
		};
		$.ajax({
			url: this.config.baseUrl + 'users.json',
			method: 'POST',
			data: data,
			success: function() { cb('success'); },
			error: function(xhr) {
				cb(xhr.status == 409 ? 'taken' : 'error');
			}
		});
	}
});
