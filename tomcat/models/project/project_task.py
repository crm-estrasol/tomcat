# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from datetime import datetime   
class TomcatProjectTask(models.Model):
    _inherit = "project.task"
    progress_rate = fields.Integer(string='Proceso actividades', compute="check_rate")
    total = fields.Integer(string="Max")
    status = fields.Selection(string="Status",
                              selection=[('done', 'Done'), ('progress', 'In Progress'), ('cancel', 'Cancel')],
                              readonly=True, track_visibility='onchange')

    maximum_rate = fields.Integer(default=100)

    def check_rate(self):
        for rec in self:
            rec.progress_rate = 0
            items = rec.timesheet_ids.filtered(lambda x: x.stage_id.id == rec.stage_id.id  )
            total = len(items.ids)
            done = 0
            cancel = 0
            # message = 'Create Work!'
            if total == 0:
                pass
            else:
                if items:
                    for item in items:
                        if item.status_t == 'done':
                            done += 1
                            # message = "Work: %s <br> Status: done" % (item.name_work)
                        if item.status_t == 'cancel':
                            cancel += 1
                            # message = "Work: %s <br> Status: cancel" % (item.name_work)
                        # if item.status == 'progress':
                        #     message = "Work: %s <br> Status: In Progress" % (item.name_work)
                    if cancel == total:
                        rec.progress_rate = 0
                    else:
                        rec.progress_rate = round(done / (total - cancel), 2) * 100
            # rec.message_post(body=message)
    """
    def check_rate(self):
        for rec in self:
            rec.progress_rate = 0
            total = len(rec.timesheet_ids.ids)
            done = 0
            cancel = 0
            # message = 'Create Work!'
            if total == 0:
                pass
            else:
                if rec.timesheet_ids:
                    for item in rec.timesheet_ids:
                        if item.status_t == 'done':
                            done += 1
                            # message = "Work: %s <br> Status: done" % (item.name_work)
                        if item.status_t == 'cancel':
                            cancel += 1
                            # message = "Work: %s <br> Status: cancel" % (item.name_work)
                        # if item.status == 'progress':
                        #     message = "Work: %s <br> Status: In Progress" % (item.name_work)
                    if cancel == total:
                        rec.progress_rate = 0
                    else:
                        rec.progress_rate = round(done / (total - cancel), 2) * 100
            # rec.message_post(body=message)
    """

class TomcatProjectTaskStage(models.Model):
    _inherit = "project.task.type"
    #activities = fields.One2many (comodel_name='check.list',inverse_name='task_id',string="Actividades")
    activities = fields.Many2many(comodel_name='check.list',relation='table_many_activities_task', column1='task_id', column2='activity_id')