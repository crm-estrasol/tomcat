# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from datetime import datetime
from dateutil.relativedelta import relativedelta

from datetime import timedelta, datetime
from odoo import tools
from odoo import api, fields, models
from odoo import fields, models
class TomCatSaleOrder(models.Model):
    _inherit  = "sale.order"
    proyect = fields.Many2one('project.project', string='Proyecto',track_visibility=True)
    product_proy = fields.Many2one('product.product', string='Productos',track_visibility=True,required=True, domain="['&',('type', '=', 'service'),('service_tracking', '=', 'project_only')]", readonly=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
 
    @api.model
    def create(self, values):
        res = super(TomCatSaleOrder, self).create(values)
        
       
        return res
   
    def write(self, values):
        body =""
        if   'order_line' in values:
            order_line = values['order_line']
           
            news = filter(lambda x:  False if isinstance(x[1], int) else  'virtu' in x[1]  , order_line)   
            news_l =  len(list(filter(lambda x:  False if isinstance(x[1], int) else  'virtu' in x[1]  , order_line) ) )  
             
            removes = filter(lambda x: x[0] == 2, order_line)   
            removes_l = len(list(filter(lambda x: x[0] == 2, order_line)  )) 
            
            modifies = filter(lambda x: x[0] == 1, order_line)   
            modifies_l = len(list( filter(lambda x: x[0] == 1  and x[0] == 1 , order_line)   ))
            
            body += "<p> Nuevo(s) </p>" if news_l > 0 else ""
            for new in  news:
                
                if new[2]['project_sections'] > 0:
                    id_proy = new[2]['project_sections']   
                    new_name = "Proyecto -" + self.env['tomcat.project.section'].search([('id','=',id_proy )])[0].name   
                elif   new[2]['display_type']  == 'line_section' :
                    new_name = "Ubicación - "+new[2]['name'] if  'name' in  new[2]  else "Sin cambio" 
                else:    
                    new_name = new[2]['name'] if  'name' in  new[2]  else "Sin cambio"
                new_qty = new[2]['product_uom_qty'] if  'product_uom_qty' in  new[2]  else "Sin cambio"
                new_price = new[2]['price_unit'] if  'price_unit' in  new[2]  else "Sin cambio" 
                body +=  """
                                    <ul class="o_mail_thread_message_tracking">
                                    
                                        <li>
                                            Producto:
                                            <span> %s </span>
                                        </li>
                                        
                                        <li>
                                            Cantidad:
                                            <span> %s </span>
                                        </li>

                                        <li>
                                            Precio:
                                            <span> %s </span>
                                        </li>
                                        
                                    
                                </ul>
                            """  % ( new_name,new_qty,new_price )    

            body += "<p> Modificado(s) </p>" if modifies_l > 0 else ""   
            for modify in  modifies: 

                prev_item = self.env['sale.order.line'].search([('id','=', modify[1])])  
                ubicacion =""
                if prev_item.display_type == 'line_section':
                    ubicacion = "Ubicación - "
                    name = ubicacion+ prev_item.name
                else:    
                    name = prev_item.product_id.name if prev_item.product_id else "Proyecto -" + str(prev_item.project_sections.name)

                price_unit = prev_item.price_unit
                product_uom_qty = prev_item.product_uom_qty
                #new
                if 'project_sections' in  modify[2]:
                    id_proy = modify[2]['project_sections']   
                    data =  self.env['tomcat.project.section'].search([('id','=',id_proy )])
                    new_name = "Proyecto -" + data[0].name if data else ""
                else:  
                      
                    fix_bug = "Sin cambio" if  modify[2]['product_id'] == "" else   modify[2]['name']
                    new_name = ubicacion + fix_bug  if  'name' in  modify[2]  else "Sin cambio"
                    _logger.info("-----------------------------------"+str(fix_bug ) )
                
                    _logger.info("-----------------------------------"+str(modify[2]['product_id'] ) )
                _logger.info("-----------------------------------"+str(values ) )
                new_qty = modify[2]['product_uom_qty'] if  'product_uom_qty' in  modify[2]  else "Sin cambio"
                new_price = modify[2]['price_unit'] if  'price_unit' in  modify[2]  else "Sin cambio"
                body +=   """
                                <ul class="o_mail_thread_message_tracking">
                                
                                    <li>
                                        Producto:
                                        <span> %s </span>
                                        <span class="fa fa-long-arrow-right" role="img" aria-label="Changed" title="Changed"></span>
                                        <span>
                                            %s
                                        </span>
                                    </li>
                                    
                                    <li>
                                        Cantidad:
                                        <span> %s </span>
                                        <span class="fa fa-long-arrow-right" role="img" aria-label="Changed" title="Changed"></span>
                                        <span>
                                            %s
                                        </span>
                                    </li>

                                    <li>
                                        Precio:
                                        <span> %s </span>
                                        <span class="fa fa-long-arrow-right" role="img" aria-label="Changed" title="Changed"></span>
                                        <span>
                                            %s
                                        </span>
                                    </li>
                                    
                                
                            </ul>
                        """  % ( name,new_name,product_uom_qty,new_qty,price_unit,new_price ) 


            body += "<p> Eliminado(s) </p>" if  removes_l > 0   else ""
            for remove in  removes:
                
                prev_item = self.env['sale.order.line'].search([('id','=', remove[1])])  
                if prev_item.display_type == 'line_section':
                    name = "Ubicación - "+ prev_item.name
                else:
                    name = prev_item.product_id.name if prev_item.product_id else "Proyecto -" +str( prev_item.project_sections.name)
                price_unit = prev_item.price_unit
                product_uom_qty = prev_item.product_uom_qty
                body +=   """
                            <ul class="o_mail_thread_message_tracking">
                            
                                <li>
                                    Producto:
                                    <span> %s </span>
                                </li>
                                
                                <li>
                                    Cantidad:
                                    <span> %s </span>
                                </li>

                                <li>
                                    Precio:
                                    <span> %s </span>
                                </li>
                                            
                          
                             </ul>
                            """  %  ( name,product_uom_qty,price_unit )               
                
        if  'order_line' in values:    
            self.message_post(body=body)
        res = super(TomCatSaleOrder, self).write(values)
        
      

        return res


    def _compute_line_data_for_template_change(self, line):
        return {
            'display_type': line.display_type,
            'name': line.name,
            'project_sections': line.project_sections if line.project_sections else False,
            'state': 'draft',
        }
    @api.onchange('product_proy')
    def _on_change_mins(self):
        product = self.env['product.product'].search( [ ('id','=', self.product_proy.id)] )
        
        clear = []
        for item in self.order_line.filtered(lambda x: x.product_id.type == 'service' and x.product_id.service_tracking == 'project_only' ):
          clear.append(  (2,item.id) )
        if len(clear) > 0:
             self.order_line = clear
        if product:    
            self.order_line = [(0,0 ,{'product_id':product.id,'name':product.name,'product_uom':product.uom_id.id}) ]
  #'fee_ids': [(0, 0, values1), (0, 0, values2) ]
class SaleReport(models.Model):
    _inherit = "sale.report"

    proyect = fields.Many2one('project.project', string='Proyecto',track_visibility=True,required=True)
    
    name_proy = fields.Char('Name proyect', readonly=True)
  