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
        
        if values['order_line']:
             _logger.info("-----------------------------------"+str(v alues['order_line'] ) )

       body =  """
            <ul class="o_mail_thread_message_tracking">
            
                <li>
                    %s
                    <span> %s </span>
                    <span class="fa fa-long-arrow-right" role="img" aria-label="Changed" title="Changed"></span>
                    <span>
                        %s
                    </span>
                </li>
            
        </ul>
        """  % ( "Poducto","pop","rep" )   

         self.message_post(body=body)
        return res
   
    def write(self, values):
        
        if values['order_line']:
             _logger.info("-----------------------------------"+str(v alues['order_line'] ) )             




        res = super(TomCatSaleOrder, self).write(values)
        
        self.message_post(body="HOLAAAAAA")

        return res