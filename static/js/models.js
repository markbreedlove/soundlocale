
var Session = Backbone.Model.extend({
    url: '/session.json'
});


var User = Backbone.Model.extend({
    url: function() {
        return '/user/' + this.id + '.json';
    }
});


var Program = Backbone.Model.extend({
});


var Programs = Backbone.Collection.extend({
    initialize: function(models, opts) {
        opts || (opts = {});
        Backbone.Collection.prototype.initialize.call(this, models, opts);
        this.meters = (opts.meters || null);
    },
    model: Program,
    url: function() {
        return '/programs/near/' + this.lat.toFixed(6) + ',' +
            this.lng.toFixed(6) + ',' + this.meters + '.json';
    },
    parse: function(response) {
        return response.programs;
    },
    setPosition: function(position) {
        this.lat = position.coords.latitude;
        this.lng = position.coords.longitude;
    },
});


var Sound = Backbone.Model.extend({
    url: function() {
        url = '/sound/' + this.id + '.json';
        if (this.authToken) {
            url += '?auth_token=' + this.authToken;
        }
        return url;
    }
});


var LocalSounds = Backbone.Collection.extend({
    initialize: function(models, opts) {
        opts || (opts = {});
        Backbone.Collection.prototype.initialize.call(this, models, opts);
        this.meters = opts.meters;
        this.userID = (opts.userID || null);
    },
    model: Sound,
    url: function() {
        var path = '/sounds/near/' + this.lat.toFixed(6) + ',' +
            this.lng.toFixed(6) + ',' + this.meters + '.json';
        if (this.userID) {
            path += '?user_id=' + this.userID;
        }
        return path;
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
    },
    setUserID: function(id) {
        this.userID = id;
    }
});


var UserSounds = Backbone.Collection.extend({
    initialize: function(models, opts) {
        opts || (opts = {});
        Backbone.Collection.prototype.initialize.call(this, models, opts);
        opts.userId && (this.userId = opts.userId);
        opts.authToken && (this.authToken = opts.authToken);
    },
    model: Sound,
    url: function() {
        return '/sounds/mine.json?auth_token=' + this.authToken;
    },
    parse: function(response) {
        return response.sounds;
    }
});
