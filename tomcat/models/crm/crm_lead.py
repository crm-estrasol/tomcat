# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
class TomCatCrmLead(models.Model):
    _inherit  = "crm.lead"
    light = fields.Integer('Semadforo',tracking=True)
    