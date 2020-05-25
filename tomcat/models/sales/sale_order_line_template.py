# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from datetime import datetime
from dateutil.relativedelta import relativedelta

class TomCatSaleOrderLineTemplate(models.Model):
    _inherit = "sale.order.template.line"
    display_type = fields.Selection(selection_add=[('line_project', 'Proyecto')], default=False)
    project_sections = fields.Many2one('tomcat.project.section', string='Proyecto',track_visibility=True)
    project =  fields.Many2one('tomcat.project', string='Sistema')
    ubication =  fields.Many2one('tomcat.ubication', string='Ubiicación')
    #ubications =  fields.Many2many(related='product_id.ubications_ids') 
    #projects  =  fields.Many2many(related='product_id.project_ids') 