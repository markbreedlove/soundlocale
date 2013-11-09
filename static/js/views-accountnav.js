
var AccountNavView = Backbone.View.extend({
    el: '#accountnav',
    template: _.template($('#accountnav-template').html()),
    initialize: function(opts) {
        this.config = opts.config;
        this.user = opts.user;
        this.router = opts.router;
        this.active = null;
    },
    events: {
        'click #logout-button': 'logout'
    },
    render: function() {
        if (this.user.id) {
            this.renderLoggedIn();
        } else {
            this.$el.html(this.template({
                username: null,
                active: this.active
            }));
        }
        return this;
    },
    renderLoggedIn: function(response) {
        var that = this;
        this.user.fetch({
            success: function() {
                that.$el.html(
                    that.template({
                        username: that.user.get('username'),
                        active: that.active
                    })
                );
            }
        });
    },
    logout: function() {
        var that = this;
        $.ajax({
            url: this.config.baseUrl + 'session.json',
            type: 'delete',
            success: function() {
                window.location = that.config.baseUrl;
            }
        });
    }
});

