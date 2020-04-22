# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from datetime import datetime
from dateutil.relativedelta import relativedelta

from datetime import timedelta, datetime
import pytz
class TomCatSaleOrder(models.Model):
    _inherit  = "sale.order"
    @api.model
    def create(self, values):
        res = super(TomCatSaleOrder, self).create(values)
        res.client_order_ref = "xxxxxx"
        return res
    @api.model
    def write(self, values):
        res = super(TomCatSaleOrder, self).write(values)
        res.client_order_ref = "yyyyyy"
        return res