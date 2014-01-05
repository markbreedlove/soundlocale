
var Router = Backbone.Router.extend({
    initialize: function(opts) {
        this.config = opts.config;
        this.user = new User();
        this.authToken = null;
        this.audioContext = opts.audioContext;
        this.anView = new AccountNavView({
            config: this.config,
            router: this,
            user: this.user}
        );
    },
    routes: {
        '': 'home',
        'program/u:id': 'userProgram',
        'mysounds': 'mysounds'
    },
    home: function() {
        var that = this;
        this.plView = new ProgramListView();
        this.authenticate(function() {
            that.anView.active = 'home';
            that.anView.render();
            that.plView.render();
        });
    },
    userProgram: function(id) {
        var that = this;
        this.slView = new SoundListView({
            config: this.config,
            audioContext: this.audioContext,
            userID: id
        });
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


/*
 * ProgramMap:  for displaying sounds in a program, or on the home page
 */
function ProgramMap(div, /* LocalSounds */ sounds, clickable, callback) {
    this.sounds = sounds;
    this.markers = {};
    this.clickable = (clickable || false);
    var that = this;
    this.map = new google.maps.Map(div, {
        zoom: 18,
        streetViewControl: false,
        panControl: false,
        draggable: false
    });
    navigator.geolocation.getCurrentPosition(function(position) {
        setMapCenterFromPosition(that.map, position);
        sounds.setPosition(position);
        sounds.fetch({
            success: function() {
                sounds.each(function(sound) {
                    that.placeMarker(sound);
                });
                if (callback) {
                    callback();
                }
            }
        });
    }, function() {
        handleGeoLocationError(that.map);
    });
}

ProgramMap.prototype.placeMarker = function(sound) {
    // Place a Google Maps marker for the sound, adding a clickthrough link
    // for the sound's user's program
    var latLng = new google.maps.LatLng(sound.get('lat'), sound.get('lng'));
    this.markers[sound.id] = new google.maps.Marker({
        map: this.map,
        position: latLng,
        title: sound.get('title'),
        clickable: this.clickable
    });
    if (this.clickable) {
        google.maps.event.addListener(
            this.markers[sound.id],
            'click',
            function() {
                window.location = '#program/u' + sound.get('user_id');
            }
        );
    }
};


/*
 * SoundEditMap: for editing single sound on user's control panel page
 */
function SoundEditMap(div, /* Sound */ sound) {
    var that = this;
    this.sound = sound;
    this.newLatLng = null;
    this.map = new google.maps.Map(div, {
        zoom: 18,
        streetViewControl: true,
        panControl: true,
        draggable: true
    });
    if (sound) {
        var latLng = new google.maps.LatLng(sound.get('lat'), sound.get('lng'));
        this.map.setCenter(latLng);
        this.marker = new google.maps.Marker({
            map: map,
            position: latLng
        });
    } else {
        navigator.geolocation.getCurrentPosition(function(position) {
            setMapCenterFromPosition(that.map, position);
        });
        this.marker = null;
    }
    google.maps.event.addListener(map, 'click', function(event) {
        that.setNewLatLng(event.latLng);
    });
}

SoundEditMap.prototype.getNewLatLng = function() {
    if (this.newLatLng) {
        return {lat: this.newLatLng.lat(), lng: this.newLatLng.lng()};
    } else {
        return false;
    }
};

SoundEditMap.prototype.setNewLatLng = function(latLng) {
    this.newLatLng = latLng;
    if (! this.marker) {
        this.marker = new google.maps.Marker({
            map: this.map,
            position: this.newLatLng
        });
    } else {
        this.marker.setPosition(this.newLatLng);
    }
};


/*
 * main
 */

function main(config, audioContext) {
    new Router({
        config: config,
        audioContext: audioContext
    });
    Backbone.history.start();
}

