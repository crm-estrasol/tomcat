# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
    
class TomcatProductBrand(models.Model):
     
    _name= 'tomcat.brand'
    _inherit =  ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    name = fields.Char('Nombre', index=True, required=True)

class TomcatProductTemplate(models.Model):
    _inherit = "product.template"
    name = fields.Char('Modelo', index=True, required=True, translate=True)
    client_model = fields.Char('Modelo cliente', index=True, required=True)
    brand = fields.Many2one('tomcat.brand', string='Marca', required=True)

   

