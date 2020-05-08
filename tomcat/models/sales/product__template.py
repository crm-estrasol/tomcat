# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
class TomcatProductTemplate(models.Model):
    _inherit = "product.template"
    name = fields.Char('Modelo', index=True, required=True, translate=True)


