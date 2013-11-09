
var Router = Backbone.Router.extend({
    initialize: function(opts) {
        this.config = opts.config;
        this.user = new User();
        this.authToken = null;
        this.anView = new AccountNavView({
            config: this.config,
            router: this,
            user: this.user}
        );
    },
    routes: {
        '': 'home',
        'mysounds': 'mysounds'
    },
    home: function() {
        var that = this;
        this.slView = new SoundListView({config: this.config});
        this.authenticate(function() {
            that.anView.active = 'home';
            that.anView.render()
            that.slView.render();
        });
    },
    mysounds: function() {
        var that = this;
        this.slView && this.slView.stop();
        this.authenticate(function(ok) {
            if (ok) {
                that.anView.active = 'mysounds';
                that.anView.render();
                if (! that.uslView) {
                    that.uslView = new UserSoundListView({
                        config: that.config,
                        user: that.user,
                        authToken: that.authToken
                    });
                }
                that.uslView.render();
            } else {
                that.navigate('', {trigger: true});
            }
        });
    },
    authenticate: function(cb) {
        var that = this;
        $.getJSON(
            this.config.baseUrl + 'auth_token.json',
            function(response) {
                that.user.id = response.user_id;
                that.authToken = response.auth_token
                cb(true);
            })
        .fail(function() {
            cb(false);
        });
    }
});


function main(config) {
    new Router({config: config});
    Backbone.history.start();
}

