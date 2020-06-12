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