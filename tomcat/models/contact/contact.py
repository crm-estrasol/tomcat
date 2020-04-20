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
    url_map = fields.Char('Enlace mapa',tracking=True)
    customer_segments = fields.Many2one("tomcat.customer.segment", string="Segmento cliente",track_visibility=True)
    intermediary_category = fields.Many2one("tomcat.intermediary.category", string="Categoria intermediario",track_visibility=True)
    #ON BUTTON ACTIONS

    #ON COMPUTE

    #ON CHANGE
