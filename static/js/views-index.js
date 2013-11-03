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
        var that = this;
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

