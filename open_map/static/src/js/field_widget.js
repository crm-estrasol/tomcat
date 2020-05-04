odoo.define('open_map_widget', function (require) {
    "use strict";
    
    
    var Widget = require('web.Widget');
    
    var AlmostCorrectWidget = Widget.extend({
    
         className: 'o_int_colorpicker',
         template: "web.datepicker",
        events: { 'change .o_datepicker_input': 'changeDatetime',
                },
       init: function (parent) {
                 this._super.apply(this, arguments);
           // console.log("holaYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
           //this._replaceElement("ASDDDD")
            //this.$el.hasClass(....) // in theory, $el is already set, but you don't know what the parent will do with it, better call super first
        },start: function () {
            this.$input = this.$('input.o_datepicker_input');
            
            },
        changeDatetime: function () {
            console.log("troquita puedri");
              this.trigger("datetime_changed");
             return;
           //this.$input.val("sssssXXXXXXXXXX");
             //this.set({'value':"sssssXXXXXXXXXX"});
            },
    });
        
        
     
    return {
        AlmostCorrectWidget: AlmostCorrectWidget,
    };
    });
    
    odoo.define('open_map', function (require) {
    "use strict";
    
    var AbstractField = require('web.AbstractField');
    var fieldRegistry = require('web.field_registry');
    var InputField    =  require('web.basic_fields');
    var AlmostCorrectWidget = require('open_map_widget');
    var mapField = InputField.InputField.extend({
       className: 'o_int_colorpicker o_input',
       events: AbstractField.prototype.events,
        init: function () {
          
            
            this.totalColors = 4;
            this.color = ""
            this._super.apply(this, arguments);
           
            
        },
            start: function(){
                var self = this;
                var prom;
               this.widget = new AlmostCorrectWidget.AlmostCorrectWidget(this);
               this.widget.on('datetime_changed', this, function () {
                   console.log("esto?aaaffffffffffa")
                         console.log(this.widget.get('value'));
                        
                   
                    
                });
                
                    var prom = this.widget.appendTo('<div>').then(()=>{
    
                         self.widget.$el.addClass(self.$el.attr('class'));
                        self._prepareInput(self.widget.$input);
                        self._replaceElement(self.widget.$el);
    
    
                        //this._setValue("pop");
    
                    }) 
                return Promise.resolve(prom).then(this._super.bind(this));
                
            },
        _prepareInput: function ($input) {
            this.$input = $input || $("<input/>");
            this.$input.addClass('o_input');
    
            var inputAttrs = { placeholder: this.attrs.placeholder || "" };
            var inputVal;
            if (this.nodeOptions.isPassword) {
                inputAttrs = _.extend(inputAttrs, { type: 'password', autocomplete: 'new-password' });
                inputVal = this.value || '';
            } else {
                inputAttrs = _.extend(inputAttrs, { type: 'text', autocomplete: this.attrs.autocomplete });
                inputVal = this._formatValue(this.value);
            }
    
            this.$input.attr(inputAttrs);
            this.$input.val(inputVal);
    
            return this.$input;
        },
         on_ready: function(){
            //  var widget = new AlmostCorrectWidget.AlmostCorrectWidget(this);
                    
              //  var prom = widget.insertAfter(this.$el).then(console.log("Promesa")) 
                //return Promise.resolve(prom).then(this._super.bind(this));
              //console.log(this.$input);
              //var widget = new AlmostCorrectWidget.AlmostCorrectWidget(this);
             //console.log(widget)
               //widget.insertAfter(this.$el); 
             //this.$el.appendTo($('.o_input'))
              //this.insertBefore(element)
             
          },
        _doDebouncedAction: function () {
            this.widget.changeDatetime();
        },
    
       
        
       _renderReadonly: function () {
          this._super.apply(this, arguments);
           console.log(  this.$input)
            console.log(  "aaaaaaaaaaaaaaa)
          this.$input.val("xdddddddd");
               // var prom = widget.insertAfter(this.$el).then(()=>{
                    
               // }) 
                // Promise.resolve(prom).then();
               //widget.insertAfter(this.$el); 
         //var widget = new AlmostCorrectWidget.AlmostCorrectWidget(this);
             //console.log(widget)
               //widget.insertAfter(this.$el); 
           // $('div').insertAfter(self.$input);
        },
        _click_e:function(ev){
             //var $target = $(ev.currentTarget);
                 //var data = $target.data();
                   console.log("entreeee")
                this.trigger_up('field_changed', {
                    dataPointID: this.record.id,
                    changes: { name:" data.val.toString()" } // account.move change
                    })
            }
            
        
       
    });
    
    fieldRegistry.add('open_map', mapField);
    
    return {
        mapField: mapField,
    };
    });
    