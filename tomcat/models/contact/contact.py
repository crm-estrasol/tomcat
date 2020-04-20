# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
class TomCatResPartner(models.Model):
    _inherit  = "res.partner"
    external_id = fields.Char('ID externo',tracking=True)
    
    #ON BUTTON ACTIONS

    #ON COMPUTE

    #ON CHANGE
