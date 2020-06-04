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
    @api.model
    def create(self,vals):
      res = super(TomcatResUser, self).create(vals) 
      partners = res.partner_avaible
      for partner in partners:
          partner.write({'user_id':res.id},True)
      return res    
    def write(self,vals):
      for partner in self.partner_avaible:
          partner.write({'user_id':False},True)
      super(TomcatResUser, self).write(vals) 
      partners = self.partner_avaible
      for partner in partners:
          partner.write({'user_id':self.id},True)
class TomcatResPartner(models.Model):
    _inherit = "res.partner"   
    @api.model
    def create(self,vals):
      res = super(TomcatResPartner, self).create(vals) 
      if 'user_id' in vals:
        res.user_id.write({ 'partner_avaible':[ (4, res.id) ] } )
      return res
    def write(self,vals,flag = False ):
      super(TomcatResPartner, self).write(vals)
      if flag == True :
        return 
      else:   
        self.env.cr.execute("SELECT * FROM table_search_partners where user_id = {}".format(self.id))
        value = self._cr.dictfetchall() 
        if value and self.user_id:
          value= value[0]
          partners = self.env['res.users'].search([('id','=',value['partner_id'])])
          partners.write( {'partner_avaible':[ (3,self.id ) ]} )
          new_partner = self.env['res.users'].search([('id','=',self.user_id.id)]) 
          new_partner.write({ 'partner_avaible':[ (4, self.id) ] } )
        elif self.user_id:
              self.user_id.partner_avaible = [(4, self.id)]     

     