
var Sound = Backbone.Model.extend({
    url: '/sound/' + this.id + '.json'
});

var LocalSounds = Backbone.Collection.extend({
    initialize: function(models, opts) {
        opts || (opts = {});
        Backbone.Collection.prototype.initialize.call(this, models, opts);
        opts.meters && (this.meters = opts.meters);
    },
    model: Sound,
    url: function() {
        return  '/sounds/near/' + this.lat + ',' + this.lng + ',' +
            this.meters + '.json';
    },
    parse: function(response) {
        return response.sounds;
    },
    setMeters: function(m) {
        this.meters = m;
    },
    setPosition: function(position) {
        this.lat = position.coords.latitude;
        this.lng = position.coords.longitude;
    }
});

