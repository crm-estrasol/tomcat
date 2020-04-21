odoo.define('my_field_widget', function (require) {
"use strict";

var AbstractField = require('web.AbstractField');
var fieldRegistry = require('web.field_registry');

var colorField = AbstractField.extend({
    className: 'o_int_colorpicker',
    tagName: 'span',
    supportedFieldTypes: ['integer'],
    events: {
        'click .o_color_pill': 'clickPill',
    },
    init: function () {
        this.totalColors = 3;
        this.color = ""
        this._super.apply(this, arguments);
    },
    _renderEdit: function () {
        this.$el.empty();
        for (var i = 0; i < this.totalColors; i++ ) {
            var className = "o_color_pill o_color_" + i;
            if (this.value === i ) {
                className += ' active';
            }
            this.$el.append($('<span>', {
                'class': className,
                'data-val': i,
            }));
        }
    },
    _renderReadonly: function () {
        console.log(this.value)
        var className = "o_color_pill active readonly o_color_" +this.value.toString();
        this.$el.append($('<span>', {
            'class': className,
        }));
    },
    clickPill: function (ev) {
        var $target = $(ev.currentTarget);
        
        var data = $target.data();
        
        this._setValue(data.val.toString());
        /*
        this.trigger_up('field_changed', {
            dataPointID: this.record.id,
            changes: { name: data.val.toString() } // account.move change
        });
        */
    }

});

fieldRegistry.add('int_color', colorField);

return {
    colorField: colorField,
};
});
