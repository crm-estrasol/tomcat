from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
class TomcatResUser(models.Model):
    _inherit = "res.users"
    partner_avaible  =  fields.Many2many(comodel_name='res.partner', relation='table_search_partners', 
    column1='partner_id', 
    column2='user_id',
    domain= [('customer_rank','>', 0),('id','not in', self.accion() )]  )

    def accion(self):
        self.env.cr.execute("SELECT * FROM table_search_partners")

        vals = self._cr.dictfetchall()
        array = [ x['user_id'] for x in vals if  x['partner_id'] != self.id  ]
        
        return array  
    