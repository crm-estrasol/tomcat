# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
<<<<<<< HEAD
class NoviasProductTemplateAttribute(models.Model):
    _inherit = "product.template.attribute.value"
    def _get_combination_name(self):
        """Exclude values from single value lines or from no_variant attributes."""
        return "-".join([ptav.name for ptav in self._without_no_variant_attributes()._filter_single_value_lines()])
class NoviasProductTemplate(models.Model):
    _inherit = "product.template"
    
    def _get_pre_selected(self):
        atributos = self.env["product.attribute"].search([])     
        return [(0,0,{ 'attribute_id':atributo.id ,'value_ids':[ (4,atributo.value_ids[0].id ) ] } ) for atributo in atributos ]
    
    attribute_line_ids = fields.One2many('product.template.attribute.line', 'product_tmpl_id', 'Product Attributes', copy=True ,default=_get_pre_selected)

  
            
=======
from datetime import datetime   
class TomcatProductBrand(models.Model):
    _name= 'tomcat.brand'
    _inherit =  ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    name = fields.Char('Nombre', index=True, required=True)
    #Pendiende darle un form
class TomcatProductProject(models.Model): 
    _name= 'tomcat.project'
    _inherit =  ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    name = fields.Char('Nombre', index=True, required=True)
    #Pendiende darle un form
class TomcatProductUbication(models.Model):
    _name= 'tomcat.ubication'
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
    ubications_ids = fields.Many2many(comodel_name='tomcat.ubication', relation='table_many_ubications', column1='ubication_id', column2='',string="Ubicaciones")
    project_ids = fields.Many2many(comodel_name='tomcat.project', relation='table_many_project', column1='project_id', column2='',string="Sistemas")


   

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
>>>>>>> staging_1
