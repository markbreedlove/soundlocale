
var AccountNavView = Backbone.View.extend({
    el: '#accountnav',
    template: _.template($('#accountnav-template').html()),
    initialize: function(opts) {
        this.config = opts.config;
        this.user = opts.user;
        this.router = opts.router;
    },
    events: {
        'click #login-button': 'goLogin',
        'click #logout-button': 'logout'
    },
    render: function() {
        if (this.user.id) {
            this.renderLoggedIn();
        } else {
            var that = this;
            $.getJSON(
                this.config.baseUrl + 'auth_token.json',
                function(response) {
                    that.user.id = response.user_id;
                    that.router.authToken = response.auth_token
                    that.renderLoggedIn();
                })
            .fail(function() {
                that.$el.html(that.template({username: null}));
            });
        }
        return this;
    },
    renderLoggedIn: function(response) {
        var that = this;
        this.user.fetch({
            success: function() {
                that.$el.html(
                    that.template({username: that.user.get('username')})
                );
            }
        });
    },
    goLogin: function() {
        window.location = this.config.baseUrl + 'login';
    },
    logout: function() {
        var that = this;
        $.ajax({
            url: this.config.baseUrl + 'session.json',
            type: 'delete',
            success: function() {
                that.user.clear();
                that.render();
            }
        });
    }
});

