var maxMeters = 50;

function volume(distance) {
    // TODO:  this is linear; try equal-power gain?
    return 1.0 - (distance / maxMeters);
}


var ProgramListView = Backbone.View.extend({
    el: '#soundlist',
    template: _.template($('#program_list_template').html()),
    initialize: function(opts) {
        _.bindAll(this, 'render', 'programMapReady');
        this.sounds = new LocalSounds({}, {meters: maxMeters});
    },
    render: function() {
        this.$el.html(this.template());
        new ProgramMap(
            $('#locale-map-canvas')[0],
            this.sounds,
            true,
            this.programMapReady
        );
    },
    programMapReady: function() {
        // Get programs from the list of sounds because we need the sounds
        // themselves in order to draw a more interesting map.  We avoid
        // doing a separate query for the list of programs by getting the
        // programs from the sound records.
        var programs = this.programsFromSounds(this.sounds);
        programs.each(function(program) {
            var $div = $('<div class="panel program">');
            this.$('#programs').append($div);
            new ProgramView({el: $div, model: program}).render();
        });
    },
    programsFromSounds: function(sounds) {
        var data = {}, models = [];
        sounds.each(function(s) {
            var program = s.get('program');
            if (! (program.id in data)) {
                data[program.id] = program;
            }
        });
        _.each(_.values(data), function(attrs) {
            models.push(new Program(attrs));
        });
        return new Programs(models);
    }
});


var ProgramView = Backbone.View.extend({
    template: _.template($('#program_template').html()),
    initialize: function(opts) {
        _.bindAll(this, 'render', 'goToProgram');
    },
    render: function() {
        var that = this;
        this.$el.html(this.template(this.model.toJSON()));
        this.$('button').on('click', function() {
            that.goToProgram(that.model.get('token'));
        });
        return this;
    },
    goToProgram: function(token) {
        window.location = '#program/' + token;
    }
});


var SoundListView = Backbone.View.extend({
    el: '#soundlist',
    template: _.template($('#local_sound_list_template').html()),
    events: {
        'click #play-button': 'play',
        'click #stop-button': 'stop'
    },
    initialize: function(opts) {
        _.bindAll(this, 'render', 'play', 'stop', 'update', 'updateList')
        this.config = opts.config;
        this.userID = opts.userID;
        this.sounds = new LocalSounds({}, {
            meters: maxMeters,
            userID: this.userID
        });
        this.program = new Program({}, {
            userID: this.userID
        });
        this.audioContext = opts.audioContext;
        this.loadingCount = 0;
        this.sources = {};
        this.gainNodes = {};
        this.programMap = null;
    },
    render: function() {
        var that = this;
        this.soundViews = {}
        this.$el.html(this.template());
        this.programMap = new ProgramMap(
            this.$('#program-map-canvas')[0],
            this.sounds,
            false
        );
        this.program.fetch({
            success: function() {
                that.$('.program-name').html(that.program.get('name'));
            }
        });
    },
    update: function(cb) {
        var that = this;
        cb || (cb = null);
        navigator.geolocation.getCurrentPosition(function(pos) {
            that.sounds.setPosition(pos);
            that.sounds.fetch({
                success: function() {
                    that.updateList(cb);
                },
                error: function(collection, xhr, options) {
                    console.log(xhr);
                }
            });
        });
    },
    updateList: function(cb) {
        var that = this;
        cb || (cb = null);
        // Add new sounds, or adjust volumes of sounds that are already
        // represented.
        this.sounds.each(function(sound) {
            if (sound.cid in that.soundViews) {
                that.soundViews[sound.cid].setDistance(sound.get('distance'));
            } else {
                var $div = $('<div class="sound panel panel-default">');
                that.$('#sounds').append($div);
                that.sources[sound.cid] =
                    that.audioContext.createBufferSource();
                that.sources[sound.cid].loop = sound.get('looping');
                if ('createGainNode' in that.audioContext) {
                    that.gainNodes[sound.cid] =
                        that.audioContext.createGainNode();
                } else {
                    that.gainNodes[sound.cid] =
                        that.audioContext.createGain();
                }
                that.sources[sound.cid].connect(
                    that.gainNodes[sound.cid]
                );
                that.gainNodes[sound.cid].connect(
                    that.audioContext.destination
                );
                that.soundViews[sound.cid] =
                    new SoundView({
                        model: sound,
                        el: $div,
                        audioContext: that.audioContext,
                        source: that.sources[sound.cid],
                        gainNode: that.gainNodes[sound.cid]
                    }).render().play();
            }
        });
        // Remove views of sounds that are no longer current.
        for (var cid in this.soundViews) {
            if (! this.sounds.get(cid)) {
                this.soundViews[cid].stop();
                this.soundViews[cid].remove();
                delete(this.soundViews[cid]);
                delete(this.sources[cid]);
                delete(this.gainNodes[cid]);
            }            
        }
        if (cb) {
            cb();
        }
    },
    decLoadingCount: function() {
        this.loadingCount--;
        if (this.loadingCount == 0) {
            this.$('#play-button').show();
        }
    },
    startTimer: function() {
        this.timer = setInterval(this.update, 10000);
    },
    play: function(event) {
        var that = this;
        $(event.target).button('toggle');
        $(event.target).button('loading');
        beep(function() {
            that.update(function() {
                $(event.target).button('reset');  // Remove "Loading..."
                that.startTimer();
                _.each(that.soundViews, function(v) {
                    v.play();
                });
            });
        });
    },
    stop: function() {
        this.$('#play-button').button('toggle');
        clearInterval(this.timer);
        _.each(this.soundViews, function(v) {
            v.stop();
        });
    }
});


var SoundView = Backbone.View.extend({
    template: _.template($('#local_sound_template').html()),
    initialize: function(opts) {
        _.bindAll(this, 'render', 'setDistance', 'play', 'stop');
        this.audioContext = opts.audioContext;
        this.source = opts.source;
        this.gainNode = opts.gainNode;
        this.buffer = null;
        this.loaded = false;
    },
    render: function() {
        var that = this;
        this.$el.html(this.template(this.model.toJSON()));
        this.setDistance(this.model.get('distance'));
        this.loadBuffer();
        return this;
    },
    setDistance: function(d) {
        var oldVolume = volume(this.model.get('distance'));
        var newVolume = volume(d);
        this.model.set('distance', d);
        this.$('.distance').html(Math.round(d));
        // TODO: Slew the volume from the current setting to the new one.
        // For now, just change the volume!
        this.gainNode.gain.value = newVolume;
    },
    loadBuffer: function() {
        var that = this;
        var url = this.model.get('url') + soundExt();
        var request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.responseType = 'arraybuffer';
        request.onload = function() {
            that.audioContext.decodeAudioData(
                request.response,
                function(buf) {
                    that.source.buffer = buf;
                },
                function() {
                    console.log('Could not decode audio from ' + url);
                }
            );
        };
        request.send();
    },
    play: function() {
        if ('noteOn' in this.source) {
            this.source.noteOn(0);
        } else {
            this.source.start(0);
        }
        return this;
    },
    stop: function() {
        if ('noteOff' in this.source) {
            this.source.noteOff(0);
        } else {
            this.source.stop(0);
        }
        // In case the user wants to play it again, need to create a new
        // source.  This is the way it's designed to work, the source being
        // analagous to a playhead
        var newsource = this.audioContext.createBufferSource();
        newsource.buffer = this.source.buffer;
        newsource.loop = this.source.loop;
        newsource.connect(this.gainNode);
        this.source = newsource;
        return this;
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
        sound.authToken = this.authToken;
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
        _.bindAll(this, 'save', 'deleteSound', 'fillCoords');
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
                id: null, lat: '', lng: '', title: '', looping: 0
            }));
            this.$('input[name=soundfile]').fileupload({
                url: this.config.baseUrl + 'sounds.json?auth_token=' +
                    this.authToken,
                dataType: 'json',
                add: function(e, data) {
                    that.$('button.save').off('click');
                    $uploadBtn = that.$('.upload-button-text');
                    data.context = that.$('button.save').click(function() {
                        if (! that.$('form').valid()) return;
                        $uploadBtn.html('processing ...');
                        data.submit()
                            .error(function(xhr, textStatus, errorThrown) {
                                // TODO:  handle different sorts of errors,
                                // once the endpoint is updated to produce
                                // more information.
                                $uploadBtn.html('upload file');
                                alert(errorThrown);
                            });
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
        this.$('button.delete').on('click', this.deleteSound);
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
                title: this.$('input[name=title]').val(),
                looping: (this.$('input[name=looping]').is(':checked') ? 1 : 0)
            }, {
                success: function() {
                    that._statusSuccess(that.$('.user-sound-buttons'), 'Saved');
                },
                error: function(model, xhr, opts) {
                    alert('Could not save your update: ' + xhr.statusText);
                }
            });
        }
    },
    _statusSuccess: function($element, message) {
        var t = _.template($('#status-success-template').html());
        var html = t({message: message});
        $element.prepend(html);
    },
    deleteSound: function() {
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

