var maxMeters = 85;

function volume(distance) {
    return 1.0 - (distance / maxMeters);
}

var SoundListView = Backbone.View.extend({
    el: '#soundlist',
    template: _.template($('#local_sound_list_template').html()),
    events: {
        'click #stop': 'stop',
        'click #update': 'update'
    },
    initialize: function(opts) {
        _.bindAll(this, 'render', 'stop', 'update', 'updateList');
        this.config = opts.config;
        this.soundViews = {}
        this.sounds = new LocalSounds({}, {meters: maxMeters});
        this.timer = setInterval(this.update, 10000);
    },
    render: function() {
        var that = this;
        this.$el.html(this.template());
        this.update();
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
        // Add new sounds, or adjust volumes of sounds that are already
        // represented.
        this.sounds.each(function(sound) {
            if (sound.id in that.soundViews) {
                that.soundViews[sound.id].setDistance(sound.get('distance'));
            } else {
                var $div = $('<div class="sound">');
                that.$('#sounds').append($div);
                that.soundViews[sound.id] =
                    new SoundView({model: sound, el: $div}).render();
            }
        });
        // Remove views of sounds that are no longer current.
        for (var id in this.soundViews) {
            if (! this.sounds.get(id)) {
                this.soundViews[id].remove();
                delete(this.soundViews[id]);
            }            
        }
    },
    stop: function() {
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
        this.$el.html(this.template(this.model.toJSON()));
        this.setDistance(this.model.get('distance'));
        return this;
    },
    setDistance: function(d) {
        var oldVolume = volume(this.model.get('distance'));
        var newVolume = volume(d);
        this.model.set('distance', d);
        // TODO: Slew the volume from the current setting to the new one.
        // For now, just change the volume!
        var audio = this.$('#' + this.model.id);
        audio[0].volume = newVolume;
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
                that.userSoundViews[sound.cid].render();
            } else {
                var div = $('<div class="user-sound">');
                that.$el.append(div);
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
        var div = $('<div class="user-sound">');
        this.$el.append(div);
        this.userSoundViews[sound.cid] =
            new UserSoundView({
                el: div,
                model: sound,
                listView: this,
                authToken: this.authToken,
                config: this.config
            }).render();
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
                        console.log('uploading');
                        data.submit();
                    });
                },
                done: function(e, data) {
                    console.log(data);
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

