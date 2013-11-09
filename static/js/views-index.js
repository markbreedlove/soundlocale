var maxMeters = 85;

function volume(distance) {
    return 1.0 - (distance / maxMeters);
}

var SoundListView = Backbone.View.extend({
    el: '#soundlist',
    template: _.template($('#local_sound_list_template').html()),
    events: {
        'click #stop': 'stop',
    },
    initialize: function(opts) {
        _.bindAll(this, 'render', 'stop', 'updateList');
        this.config = opts.config;
        this.sounds = new LocalSounds({}, {meters: maxMeters});
        this.playing = false;
    },
    render: function() {
        var that = this;
        this.soundViews = {}
        this.$el.html(this.template());
        this.playing = true;
        this.update();
        this.startTimer();
    },
    update: function() {
        var that = this;
        navigator.geolocation.getCurrentPosition(function(pos) {
            that.sounds.setPosition(pos);
            that.sounds.fetch({
                success: that.updateList,
                error: function(collection, xhr, options) {
                    console.log(xhr);
                }
            });
        });
    },
    updateList: function() {
        var that = this;
        if (! this.playing) return;
        // Add new sounds, or adjust volumes of sounds that are already
        // represented.
        this.sounds.each(function(sound) {
            if (sound.cid in that.soundViews) {
                that.soundViews[sound.cid].setDistance(sound.get('distance'));
            } else {
                var $div = $('<div class="sound panel panel-default">');
                that.$('#sounds').append($div);
                that.soundViews[sound.cid] =
                    new SoundView({model: sound, el: $div}).render();
            }
        });
        // Remove views of sounds that are no longer current.
        for (var cid in this.soundViews) {
            if (! this.sounds.get(cid)) {
                this.soundViews[cid].remove();
                delete(this.soundViews[cid]);
            }            
        }
    },
    startTimer: function() {
        this.timer = setInterval(this.update, 10000);
    },
    stop: function() {
        this.playing = false;
        clearInterval(this.timer);
        $audios = $('audio');
        for (var i = 0; i < $audios.length; i++) {
            $audios[i].pause();
        }
    }
});


var SoundView = Backbone.View.extend({
    template: _.template($('#local_sound_template').html()),
    initialize: function() {
        _.bindAll(this, 'render', 'setDistance');
    },
    render: function() {
        var that = this;
        this.$el.html(this.template(this.model.toJSON()));
        this.setDistance(this.model.get('distance'));
        // There's something like a race condition in Chrome that is solved
        // by the following timeout, along with the <audio> element not being
        // set to autoplay.
        setTimeout(function() {
            that.$('audio')[0].play();
        }, 500);
        return this;
    },
    setDistance: function(d) {
        var oldVolume = volume(this.model.get('distance'));
        var newVolume = volume(d);
        this.model.set('distance', d);
        // TODO: Slew the volume from the current setting to the new one.
        // For now, just change the volume!
        this.$('audio')[0].volume = newVolume;
    }
});


var UserSoundListView = Backbone.View.extend({
    el: '#soundlist',
    initialize: function(opts) {
        _.bindAll(this, 'renderSoundViews');
        this.config = opts.config;
        this.user = opts.user;
        this.authToken = opts.authToken;
        this.userSounds = new UserSounds({}, {
            userId: opts.user.id,
            authToken: opts.authToken
        });
        this.userSoundViews = {};
    },
    template: _.template($('#user_sound_list_template').html()),
    events: {
        'click #add-sound': 'addSound'
    },
    render: function() {
        this.$el.html(this.template({}));
        this.userSounds.fetch({
            success: this.renderSoundViews,
            error: function(collection, response, options) {
                alert(response.statusText);
            }
        });
        return this;
    },
    renderSoundViews: function() {
        var that = this;
        this.userSounds.each(function(sound) {
            sound.authToken = that.authToken;
            if (that.userSoundViews[sound.cid]) {
                var v = that.userSoundViews[sound.cid];
                if (v.$el.parentNode) {  // if it's in the document
                    that.userSoundViews[sound.cid].render();
                } else {                 // else, re-append it
                    that.$el.append(v.$el);
                }
            } else {
                var div = $('<div class="user-sound panel panel-default">');
                that.$('#user-sounds').append(div);
                that.userSoundViews[sound.cid] =
                    new UserSoundView({
                        el: div,
                        model: sound,
                        listView: that,
                        authToken: that.authToken,
                        config: that.config
                    }).render();
            }
        });
    },
    addSound: function() {
        var sound = new Sound({}, {authToken: this.authToken});
        var div = $('<div class="user-sound panel panel-default">');
        div.css({display: 'none'});
        this.$('#user-sounds').prepend(div);
        this.userSoundViews[sound.cid] =
            new UserSoundView({
                el: div,
                model: sound,
                listView: this,
                authToken: this.authToken,
                config: this.config
            }).render();
        div.slideDown();
    }
});


var UserSoundView = Backbone.View.extend({
    initialize: function(opts) {
        _.bindAll(this, 'save', 'delete', 'fillCoords');
        opts || (opts = {});
        opts.authToken && (this.authToken = opts.authToken);
        opts.config && (this.config = opts.config);
    },
    template: _.template($('#user_sound_template').html()),
    render: function() {
        var that = this;
        var params;
        if (this.model.isNew()) {
            this.$el.html(this.template({
                id: null, lat: '', lng: '', title: ''
            }));
            this.$('input[name=soundfile]').fileupload({
                url: this.config.baseUrl + 'sounds.json?auth_token=' +
                    this.authToken,
                dataType: 'json',
                add: function(e, data) {
                    that.$('button.save').off('click');
                    data.context = that.$('button.save').click(function() {
                        if (! that.$('form').valid()) return;
                        data.submit();
                    });
                },
                done: function(e, data) {
                    that.model.set(data.result);
                    that.render();
                },
            });
        } else {
            this.$el.html(this.template(this.model.toJSON()));
            this.$('button.save').on('click', this.save);
        }
        this.$('button.delete').on('click', this.delete);
        this.$('button.use-current-coords').on('click', this.fillCoords);
        this.$('form').validate({
            rules: {
                lat: { number: true },
                lng: { number: true }
            }
        });
        return this;
    },
    save: function() {
        var that = this;
        if (! this.$('form').valid()) return;
        if (this.model.isNew()) {
            console.log('SHOULD NOT BE REACHED');
        } else {
            this.model.save({
                lat: this.$('input[name=lat]').val(),
                lng: this.$('input[name=lng]').val(),
                title: this.$('input[name=title]').val()
            }, {
                success: function() { /* TODO: indicate success */ },
                error: function(model, xhr, opts) {
                    alert('Could not save your update: ' + xhr.statusText);
                }
            });
        }
    },
    delete: function() {
        var that = this;
        if (confirm('Really delete this sound?')) {
            this.model.destroy({
                success: function() {
                    that.$el.slideUp();
                    that.remove();
                },
                error: function(model, xhr, options) {
                    alert('Could not delete the sound: ' + xhr.statusText);
                }
            });
        }
    },
    fillCoords: function() {
        var that = this;
        navigator.geolocation.getCurrentPosition(function(pos) {
            that.$('input[name=lat]').val(pos.coords.latitude);
            that.$('input[name=lng]').val(pos.coords.longitude);
        });
    }
});

