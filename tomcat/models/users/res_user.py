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
    def write(self,vals,flag = False ):
      #_logger.info("-----------------------------------"+str(vals['partner_avaible']) )
      originals = [x.id for x in  self.partner_avaible]
      #for partner in self.partner_avaible:
      #    partner.write({'user_id':False},True)
      super(TomcatResUser, self).write(vals) 
      if flag:
        return 
      if 'partner_avaible' in  vals:
        originals_eliminated = [x for x in  originals if x not in  vals['partner_avaible'][0][2]   ]
        new = [x for x in  vals['partner_avaible'][0][2] if x not in  originals   ]
        eliminated = self.env['res.partner'].search([('id','in',originals_eliminated)])
        news = self.env['res.partner'].search([('id','in',new)])
        for item in eliminated:
          item.write({'user_id':False},False)
        for item in news:
          item.write({'user_id':self.id},False)
class TomcatResPartner(models.Model):
    _inherit = "res.partner"   
    @api.model
    def create(self,vals):
      res = super(TomcatResPartner, self).create(vals) 
      
      usr = self.env['res.users'].search([('id','=',res.user_id.id)])
      if usr:
        usr.write({ 'partner_avaible':[ (4, res.id) ] },True )
      return res
    
    def write(self,vals,flag = False ):
      original_id = int(self.id)
      original_user =   int(self.user_id.id)
      super(TomcatResPartner, self).write(vals)
      if flag  :
        return 
      if original_user == self.user_id.id:
           return 
      elif self.user_id:  
          #Last user relation        
          value = self.env.cr.execute("SELECT * FROM table_search_partners where user_id = {}".format(original_id))
          value = self._cr.dictfetchall() 
          #new user
          partners_original = self.env['res.users'].search([('id','=',self.user_id.id)])
          if  len(value) == 0:   
              partners_original.write( {'partner_avaible':[  (4, self.id) ] },True )
              return 
          value= value[0]
          #last user orignal
          partners = self.env['res.users'].search([('id','=',value['partner_id'])])
          partners.write( {'partner_avaible':[ (3,self.id )  ]},True )
          partners_original.write( {'partner_avaible':[ (4,self.id )  ]},True )
      else:
        value = self.env.cr.execute("SELECT * FROM table_search_partners where user_id = {}".format(original_id))
        value = self._cr.dictfetchall() 
        if value:
          value = value[0]
          partners = self.env['res.users'].search([('id','=',value['partner_id'])])
          partners.write( {'partner_avaible':[ (3,self.id )  ]},True )







        
          
       
        
     