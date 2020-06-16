# -*- coding: utf-8 -*-

from odoo import models, fields


class CheckList(models.Model):
    _name = 'check.list'
    name = fields.Char('Nombre trabajo')
    name_work = fields.Text('Name Work', track_visibility='onchange', invisible="1")
    description = fields.Text(string="Descripción")
    task_id = fields.Many2one('project.task.type', string='Etapa' , readonly="1")