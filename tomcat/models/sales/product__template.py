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
    #Pendiende darle un form
class TomcatProductTemplate(models.Model):
    _inherit = "product.template"
    name = fields.Char('Modelo', index=True, required=True, translate=True)
    client_model = fields.Char('Modelo cliente', index=True, required=True)
    brand = fields.Many2one('tomcat.brand', string='Marca', required=True)
    margin_ut = fields.Float("Margen %",  store=True, digits=(12, 6))


   
class TomcatTestItem(models.Model):
    _inherit = "product.pricelist.item"
    cost =fields.Float(realetd="product_id.standard_price", readonly=True)
    margin_ut = fields.Float("Margen %",  store=True, digits=(12, 6))
    @api.onchange('margin_ut' )
    def product_uom_change(self):
        self.fixed_price =  self.cost / (1 - self.margin_ut )
class PricelistItemTomCat(models.Model):
    _inherit = "product.pricelist.item"
    cost = fields.Float(realetd="product_id.standard_price",readonly=True)
    margin_ut = fields.Float("Margen %",  store=True, digits=(12, 6))
    
    @api.onchange('margin_ut')
    def product_uom_change(self):
        self.fixed_price = self.cost / (1 - self.margin_ut) 