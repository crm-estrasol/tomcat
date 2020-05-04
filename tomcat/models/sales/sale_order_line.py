# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from datetime import datetime
from dateutil.relativedelta import relativedelta

class TomPCatProjectSection(models.Model):
    _name = 'tomcat.project.section'
    _rec_name = 'name'
    name = fields.Char("Nombre")
  



class TomCatSaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    product_id = fields.Many2one(
        'product.product', string='Product', domain="[('sale_ok', '=', True),'&',('type', '!=', 'service'),('service_tracking', '!=', 'project_only'), '|', ('company_id', '=', False), ('company_id', '=', parent.company_id)]",
        change_default=True, ondelete='restrict', check_company=True)  # Unrequired company
    display_type = fields.Selection(selection_add=[('line_project', 'Proyecto')], default=False)
    
    
    project_sections = fields.Many2one('tomcat.project.section', string='Proyecto',track_visibility=True)
    type_proyect  = fields.Selection(related='product_id.service_tracking')