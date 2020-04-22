# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from datetime import datetime
from dateutil.relativedelta import relativedelta

from datetime import timedelta, datetime
import pytz
class TomCatSaleOrder(models.Model):
    _inherit  = "sale.order"
    @api.model
    def create(self, values):
        res = super(TomCatSaleOrder, self).create(values)
        
       
        return res
   
    def write(self, values):
        body =""
        if values['order_line']:
            order_line = values['order_line']
            news = filter(lambda x:  False if isinstance(x[1], int) else  'virtu' in x[1]  , order_line)   
             
            deletes = filter(lambda x: x[0] == 2, order_line)   
            
            modifies = filter(lambda x: x[0] == 1, order_line)   
            
            for modify in  modifies: 
                prev_item = self.env['sale.order.line'].search([('id','=', modify[1])])  
                name = prev_item.product_id.name
                price_unit = prev_item.price_unit
                product_uom_qty = prev_item.product_uom_qty
                #new
                new_name = modify[2]['name'] if  'name' in  modify[2]  else "Sin cambio"
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
                                    
                                    
                                
                            </ul>
                        """  % ( name,new_name ) 
                

               
                _logger.info("------------------Modifica-----------------"+str( str(modify[2]) ) )            
            

        res = super(TomCatSaleOrder, self).write(values)
        
        self.message_post(body=body)

        return res

"""
    4 ,_ ,False //NADA
    2 ,id , ---------------elimina 
    0 , virtual ----------- nuevo 
    1,id, diccionario ---------Editar 

"""