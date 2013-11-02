
var Router = Backbone.Router.extend({
    initialize: function(opts) {
        this.config = opts.config;
        this.user = new User();
        this.anView = new AccountNavView({
            config: this.config,
            user: this.user}
        ).render();
    },
    routes: {
        '': 'home'
    },
    home: function() {
        this.slView || (this.slView = new SoundListView({config: this.config}));
        this.slView.render();
    }
});


function main(config) {
    new Router({config: config});
    Backbone.history.start();
}

