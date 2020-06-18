# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from datetime import datetime   
class TomcatHelpDesk(models.Model):
    _inherit = "helpdesk.ticket"
    #progress_rate = fields.Integer(string='Proceso actividades', compute="check_rate")
    #progress_global = fields.Integer(string='Proceso actividades', compute="check_rate_global")
    #otal = fields.Integer(string="Max")
    #tatus = fields.Selection(string="Status",
    #                          selection=[('done', 'Done'), ('progress', 'In Progress'), ('cancel', 'Cancel')],
    #                         readonly=True, track_visibility='onchange')

    #maximum_rate = fields.Integer(default=100)

