# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
class TomCatCrmLead(models.Model):
    _inherit  = "crm.lead"
    light = fields.Integer('Semadforo',tracking=True,default=0 )
    light_help = fields.Integer('Semadforo temo',tracking=True,default=0, compute='_compute_show_light' )
    #ON BUTTON ACTIONS

    #ON COMPUTE

    #ON CHANGE
  
    def _compute_show_light(self):
       num_days = self.env['ir.config_parameter'].sudo().get_param('intelli.limit_days')
       for record in self:
           op = record
           
           limit_contact = op.activity_ids[0].create_date + relativedelta(days=int(num_days))
           real_difference =   (limit_contact - datetime.today()).days      
           
           if  real_difference <= 5 :
              record.light_help = 3 
              record.write({'light':3})
           if  real_difference > 6  and real_difference <= 10 :
              record.light_help = 2 
              record.write({'light':2})
           if  real_difference >= 11  :
              record.light_help = 3 
              record.write({'light':3})   
          

            
        