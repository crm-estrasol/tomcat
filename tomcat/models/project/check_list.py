# -*- coding: utf-8 -*-

from odoo import models, fields


class CheckList(models.Model):
    _name = 'check.list'
    name = fields.Char('Name')
    name_work = fields.Text('Name Work', track_visibility='onchange')
    description = fields.Text('Description')
    task_id = fields.Many2one('project.task.type', string='Etapa' , readonly="1")