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
    discount = fields.Float(help="Discount",digits=(16, 2) ,store=True)
    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        super(TomcatPurchaseLine, self)._onchange_quantity()
        self.apply_discount()
    @api.onchange('discount')    
    def apply_discount(self):
        if self.discount > 0:
            original = self.price_unit
            self.price_subtotal =  original  - (self.original * (self.discount / 100) )
    