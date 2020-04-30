
odoo.define('light_control.tomcat_sale_order_line', function (require) {
   
    
    "use strict";
 
    var SectionAndNoteListRenderer = require('account.section_and_note_backend');
  
    var  a = SectionAndNoteListRenderer
  
    SectionAndNoteListRenderer.include({
        /**
         * We want section and note to take the whole line (except handle and trash)
         * to look better and to hide the unnecessary fields.
         *
         * @override
         */
        _renderBodyCell: function (record, node, index, options) {
            
            var $cell = this._super.apply(this, arguments);
    
            var isSection = record.data.display_type === 'line_section';
            var isNote = record.data.display_type === 'line_note';
            var isProject = record.data.display_type === 'line_project';
          
          
                   
            var nbrColumns = this._getNumberOfCols();
             
            if( node.attrs.name === "project_sections" && isProject){
                var nbrColumns = this._getNumberOfCols();

                return $cell.removeClass('o_hidden').attr('colspan',nbrColumns);
            }
            
            if( node.attrs.name === "name" && isProject){
                var nbrColumns = this._getNumberOfCols();

                return $cell.addClass('o_hidden').attr('colspan',0);
                
            }

            else{
                return $cell;
            }
        },
        /**
         * We add the o_is_{display_type} class to allow custom behaviour both in JS and CSS.
         *
         * @override
         */
        _renderRow: function (record, index) {
            var $row = this._super.apply(this, arguments);
    
            if (record.data.display_type) {
                $row.addClass('o_is_' + record.data.display_type);
            }

    
            return $row;
        },
        /**
         * We want to add .o_section_and_note_list_view on the table to have stronger CSS.
         *
         * @override
         * @private
         */
        _renderView: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.$('.o_list_table').addClass('o_section_and_note_list_view');
                self.$('.o_list_table').find("thead [data-name='project_sections']").toggle();
            });
        }
    });
    
   
    });
    