# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
class TomCatCustomerSegment(models.Model):
   _name = 'tomcat.customer.segment'
   _inherit =  ['mail.thread', 'mail.activity.mixin']
   _rec_name = 'name'
   name = fields.Char("Nombre")
   def init(self):
      try:
         items = self.env['tomcat.customer.segment'].search([])
         if not items:
            values = [
                     "BARES Y RESTAURANTES",
                     "COMERCIAL",
                     "CORPORATIVO",
                     "EDUCACION",
                     "HOSPITALITY",
                     "INDUSTRIAL",
                     "RESIDENCIAL",
                     "SALUD"
                     ]
            for val in values:
               self.env['tomcat.customer.segment'].create({'name':val})
      except:
         pass
