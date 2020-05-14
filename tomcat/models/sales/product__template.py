# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from datetime import datetime   
class TomcatProductBrand(models.Model):
     
    _name= 'tomcat.brand'
    _inherit =  ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    name = fields.Char('Nombre', index=True, required=True)
    #Pendiende darle un form
class TomcatProductTemplate(models.Model):
    _inherit = "product.template"
    name = fields.Char('Modelo', index=True, required=True, translate=True)
    client_model = fields.Char('Modelo cliente', index=True)
    brand = fields.Many2one('tomcat.brand', string='Marca')
    margin_ut = fields.Float("Margen %",  store=True, digits=(12, 6))


   

class PricelistItemTomCat(models.Model):
    _inherit = "product.pricelist.item"
    cost = fields.Float(related="product_tmpl_id.standard_price")
    

    margin_ut = fields.Float("Margen %",  store=True, digits=(12, 6))
    
    @api.onchange('margin_ut')
    def product_uom_change(self):
        cost = self.cost
        if self.pricelist_id.currency_id.name == "USD": 
            cur = self.env['res.currency'].search([('name', '=', 'MXN')]) 
            cur_dlr = self.env['res.currency'].search([('name', '=', 'USD')]) 
            cost = cur._convert( self.cost , cur_dlr, self.env.company, date=datetime.today(), round=False)
        margin_fix = self.margin_ut / 100
        self.fixed_price = cost / (1 - margin_fix)  
    @api.onchange('pricelist_id')
    def product_pricelist(self):
         self.fixed_price = 0
         self.margin_ut = 0
