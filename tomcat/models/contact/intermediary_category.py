# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
class TomCatIntermediaryCategory(models.Model):
   _name = 'tomcat.intermediary.category'
   _inherit =  ['mail.thread', 'mail.activity.mixin']
   _rec_name = 'name'
   name = fields.Char("Nombre")
   def init(self):
      try:
         items = self.env['tomcat.intermediary.category'].search([])
         if not items:
            values = [
                     "CLIENTE FINAL",
                     "TALLER DE ARQUITECTURA",
                     "DISEÑO DE INTERIORES",
                     "CONSTRUCTORA",
                     "COMISIONISTA",
                     "PARTNER",
                     "ADMINISTRADORA DE PROYECTO"

                     ]
            for val in values:
               self.env['tomcat.intermediary.category'].create({'name':val})
      except:
         pass