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

    """
    @api.depends('product_qty', 'price_unit', 'taxes_id','discount')
    def _compute_amount(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            taxes = line.taxes_id.compute_all(
                vals['price_unit'],
                vals['currency_id'],
                vals['product_qty'],
                vals['product'],
                vals['partner'])
            #if taxes['total_excluded'] != 0 and vals['discount'] > 0:
            #    fix_price = taxes['total_excluded'] - ( taxes['total_excluded'] *  (vals['discount'] / 100) )
            #else:
            #    fix_price = taxes['total_excluded']
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal':  taxes['total_excluded'],
            })
   """
           
    def _prepare_compute_all_values(self):
        # Hook method to returns the different argument values for the
        # compute_all method, due to the fact that discounts mechanism
        # is not implemented yet on the purchase orders.
        # This method should disappear as soon as this feature is
        # also introduced like in the sales module.
        res = super(TomcatPurchaseLine, self)._prepare_compute_all_values()
      
        res['price_unit'] = self.price_unit - self.price_unit * (self.discount/100)
        
        return res 
        """
        #self.ensure_one()
        return {
            'price_unit': self.price_unit - self.price_unit * (self.discount/100) ,
            'currency_id': self.order_id.currency_id,
            'product_qty': self.product_qty,
            'product': self.product_id,
            'partner': self.order_id.partner_id,
            'discount': self.discount,
        }
        """