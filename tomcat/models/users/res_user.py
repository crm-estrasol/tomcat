from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
class TomcatResUser(models.Model):
    _inherit = "res.users"
    partner_avaible  =  fields.Many2many(comodel_name='res.partner', relation='table_search_partners', 
    column1='partner_id', 
    column2='user_id',
      )
    partner_Navaible  =  fields.Many2many(comodel_name='res.partner', relation='table_search_partemp', 
    column1='partner_id', 
    column2='user_id',
    compute='_accion'
      )

    def _accion(self):
        self.env.cr.execute("SELECT * FROM table_search_partners")
        vals = self._cr.dictfetchall()
        for item in self:
            array = [ x['user_id'] for x in vals if  x['partner_id'] != item.id  ]
            item.partner_Navaible = [ (4,x ) for x in array ] 
    def create(self,vals):
      res = super(TomcatResUser, self).create(vals) 
      partners = res.partner_avaible
      for partner in partners:
          partner.user_id = res.id
    def write(self,vals):
      super(TomcatResUser, self).write(vals) 
      partners = self.partner_avaible
      for partner in partners:
          partner.user_id = self.id
        