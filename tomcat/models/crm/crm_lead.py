# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
import random
class TomCatCrmLead(models.Model):
    _inherit  = "crm.lead"
    light = fields.Integer('Semadforo',tracking=True,default=0 )
    light_help = fields.Integer('Semadforo temo',tracking=True,default=0, compute='_compute_show_light' )
    #ON BUTTON ACTIONS

    #ON COMPUTE

    #ON CHANGE
  
    def _compute_show_light(self):
       for record in self:
            rand  =  random.randint(1,3)
            record.light_help = 
            record.write({'light':rand})
        