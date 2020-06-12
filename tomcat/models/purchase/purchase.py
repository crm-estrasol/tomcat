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
 
    @api.depends('product_qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            taxes = line.taxes_id.compute_all(
                vals['price_unit'],
                vals['currency_id'],
                vals['product_qty'],
                vals['product'],
                vals['partner'])
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'] * 2,
            })
    
    