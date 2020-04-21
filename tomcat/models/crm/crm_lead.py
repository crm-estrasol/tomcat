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
       num_days = int(self.env['ir.config_parameter'].sudo().get_param('intelli.limit_days'))
       num_one = num_days
       num_two = num_days*-1
       num_three = num_days*2*-1
       for record in self:
           op = record
           if  op.activity_ids:
                limit_contact = (datetime.today() - relativedelta(days=int(10) ) )  + relativedelta(days=int(num_days))
                real_difference =   int( (limit_contact - datetime.today()).days )       
                
                if   real_difference >= 0 and  real_difference <= num_one :
                        record.light_help = 3 
                        record.write({'light':3})
                elif  real_difference < 0  and real_difference >= num_two :
                        record.light_help = 2 
                        record.write({'light':2})
                elif  real_difference <= (num_three+1)  :
                        record.light_help = 1 
                        record.write({'light':1})   
           else:
                 record.light_help = 0 
                 record.write({'light':0})      

            
        