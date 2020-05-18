# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class SaleDiscount(models.TransientModel):
    _name = 'tomcat.sale.discount.wizard'
    _description = 'Descuentos '
    projects =  fields.Many2many(comodel_name='tomcat.project', relation='table_many_project_2', column1='project_id', column2='',string="Sistema")
    ubications =  fields.Many2many(comodel_name='tomcat.ubication', relation='table_many_ubication_2', column1='ubication_id', column2='',string="Ubicaciones")
    brand =  fields.Many2many(comodel_name='tomcat.brand', relation='table_many_brand', column1='brand_id', column2='',string="Marcas")
    discount =  fields.Float("Descuento",digits=(16, 2) )
    sale = fields.Many2one('sale.order', string='Venta')

    def generate_report(self):
        data = {'date_start':self.start_date, 'date_stop': self.end_date, 'config_ids': ""}
        return self.env.ref('tomcat.sale_details_report_dos').report_action([], data=data)
    