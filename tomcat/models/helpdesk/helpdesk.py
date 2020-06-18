# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from datetime import datetime   
class TomcatHelpDesk(models.Model):
    _inherit = "helpdesk.ticket"
    activity_done = fields.Text(string="Actividades")
    cause = fields.Text(string="Causas problema ")
    observation = fields.Text(string="Observaciones ")
    service_quaranty = fields.Selection([('yes', 'Si'), ('no', 'No')], string='Servicio entra en garantía',default="no")
    service_days  = fields.Selection([('yes', 'Si'), ('no', 'No')], string='Servicio requiera mas días', default='no')
    expected_date =  fields.Datetime(string='Fecha estimada de entrega', default=fields.Datetime.now)

