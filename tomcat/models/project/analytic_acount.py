# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from datetime import datetime   
class TomcatAnalyticAcount(models.Model):
    _inherit = "account.analytic.line"
    name_work = fields.Text('Nombre trabajo')
    status_t = fields.Selection(string="Estatus",
                              selection=[('done', 'Hecho'), ('progress', 'En progreso'), ('cancel', 'Cancelado')],
                              readonly=True)
    stage_id = fields.Many2one('project.task.type', string='Etapa',invisible=True)
    show_stage  =   fields.Many2one(related="stage_id")

    def do_accept(self):
        self.write({
            'status_t': 'done',
        })
        # return {'type': 'ir.actions.client', 'tag': 'reload'}

    def do_cancel(self):
        self.write({
            'status_t': 'cancel',
        })
        # return {'type': 'ir.actions.client', 'tag': 'reload'}

    def do_progress(self):
        self.write({
            'status_t': 'progress',
        })
        # return {'type': 'ir.actions.client', 'tag': 'reload'}

    def do_set_to(self):
        self.write({
            'status_t': ''
        })
#WIZARD

class  ProjectTaskCreateTimesheet(models.TransientModel):
    _inherit = 'project.task.create.timesheet'
     
    def save_timesheet(self):
        res = super(ProjectTaskCreateTimesheet, self).save_timesheet()
        res.stage_id = self.task_id.stage_id.id
        return res