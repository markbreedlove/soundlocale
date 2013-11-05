
var Router = Backbone.Router.extend({
    initialize: function(opts) {
        this.config = opts.config;
        this.user = new User();
        this.authToken = null;
        this.anView = new AccountNavView({
            config: this.config,
            router: this,
            user: this.user}
        ).render();
    },
    routes: {
        '': 'home',
        'mysounds': 'mysounds'
    },
    home: function() {
        this.slView || (this.slView = new SoundListView({config: this.config}));
        this.slView.render();
    },
    mysounds: function() {
        if (! this.uslView) {
            this.uslView = new UserSoundListView({
                config: this.config,
                user: this.user,
                authToken: this.authToken
            });
        }
        this.uslView.render();
    }
});


function main(config) {
    new Router({config: config});
    Backbone.history.start();
}

