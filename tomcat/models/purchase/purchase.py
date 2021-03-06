# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from datetime import datetime   
class TomcatPurchase(models.Model):
    _inherit = "purchase.order"
    external_document = fields.Boolean('Cotización externa', default=False,track_visibility=True)
    external_number = fields.Char('Número pedido proveedor', default=False,track_visibility=True)
    def action_rfq_send(self):
        values = super(TomcatPurchase,self).action_rfq_send()
        ctx = values['context']
        ctx['default_external_document'] =  self.external_document 
        ctx['default_purchase'] = True
        values['context'] = ctx 
        return values 
class TomcatPurchaseLine(models.Model):
    _inherit = "purchase.order.line"
    discount = fields.Float(help="Discount",digits=(16, 2) ,store=True,string="Descuento")
    brand = fields.Many2one(related="product_id.brand")
    
    def _prepare_compute_all_values(self):
       
        res = super(TomcatPurchaseLine, self)._prepare_compute_all_values()
      
        res['price_unit'] = self.price_unit - self.price_unit * (self.discount/100)
        
        return res 
    @api.onchange('discount')
    def _on_change_discount(self):
        #self.price_subtotal = self.price_unit - self.price_unit * (self.discount/100)
        self._compute_amount()

    def _get_product_purchase_description(self, product_lang):
        self.ensure_one()
        name=""
        if product_lang.description_purchase:
            name += product_lang.description_purchase
        return name