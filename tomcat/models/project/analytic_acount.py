# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from datetime import datetime   
class TomcatAnalyticAcount(models.Model):
    _inherit = "account.analytic.line"
    name_work = fields.Text('Nombre trabajo')
    status_t = fields.Selection(string="Status",
                              selection=[('done', 'Hecho'), ('progress', 'En progreso'), ('cancel', 'Cancelado')],
                              readonly=True)