# -*- coding: utf-8 -*-

from odoo import models, fields


class CheckList(models.Model):
    _name = 'check.list'
    name = fields.Char('Name')
    name_work = fields.Text('Name Work', track_visibility='onchange')
    description = fields.Text('Description')