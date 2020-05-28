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
import sys
import itertools
from operator import itemgetter
import functools 
#Filtrar
from collections import deque
import json
from odoo import http
from odoo.http import request
from odoo.tools import ustr
from odoo.tools.misc import xlwt
#XLS
import xlwt
import base64
from io import BytesIO

class TomCatSaleOrder(models.Model):
    _inherit  = "sale.order"
    proyect = fields.Many2one('project.project', string='Proyecto',track_visibility=True)
    product_proy = fields.Many2one('product.product', string='Plantilla proyecto',track_visibility=True,required=True, domain="['&',('type', '=', 'service'),('service_tracking', '=', 'project_only')]", readonly=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    name_proy = fields.Char('Nombre proyecto',track_visibility=True, required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    print_options = fields.Selection([('complete_total', 'Completo  totalizado'), 
                                                ('only_complete', 'Completo') , ('complete_price', 'Completo precio unitario'), ('no_brandModel','Sin marca y modelo') ,
                                                ('without_price', 'Sin precios'),('subtotal_system', 'Solo con subtotal por sistema')], string='Formato pdf', copy=False, default='only_complete')
    client_model = fields.Boolean( string='Modelo cliente')
    
    @api.model
    def create(self, values):
        
       
        res = super(TomCatSaleOrder, self).create(values)
        res.write({'name':res.name+"-"+res.name_proy})
        if  'product_proy' in values:  
            product = self.env['product.product'].search( [ ('id','=', values['product_proy'])] )
            res.order_line =  [ (0,0 ,{'product_id':product.id,'name':product.name,'product_uom':product.uom_id.id}) ]
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
            modifies_l = len(list( filter(lambda x: x[0] == 1  , order_line)   ))
            
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
                      
                    #fix_bug = "Sin cambio" if not 'product_id'  in modify[2] else   modify[2]['name']
                    
                    new_name = ubicacion + modify[2]['name'] if  'name' in  modify[2]  else "Sin cambio"
                   
                
                
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
        if  'product_proy' in values:   
            news = []
           
            for item in self.order_line.filtered(lambda x: x.product_id.type == 'service' and x.product_id.service_tracking == 'project_only' ):
                news.append(  (2,item.id) )
            
            product = self.env['product.product'].search( [ ('id','=', values['product_proy'])] )
            news.append( (0,0 ,{'product_id':product.id,'name':product.name,'product_uom':product.uom_id.id}) )
            self.order_line = news


        
      

        return res


    def _compute_line_data_for_template_change(self, line):
        return {
            'display_type': line.display_type,
            'name': line.name,
            'project_sections': line.project_sections if line.project_sections else False,
            'state': 'draft',
        }
    
    """
    @api.onchange('product_proy')
    def _on_change_mins(self):
        _logger.info("-----------------------------------"+str(self.order_line) )
        product = self.env['product.product'].search( [ ('id','=', self.product_proy.id)] )
        
        news = []
        for item in self.order_line.filtered(lambda x: x.product_id.type == 'service' and x.product_id.service_tracking == 'project_only' ):
          news.append(  (2,item.id) )
     
        if product:    

            news.append( (0,0 ,{'product_id':product.id,'name':product.name,'product_uom':product.uom_id.id}) )
            self.order_line = news 
        _logger.info("-----------------------------------"+str(self.order_line) )
  #'fee_ids': [(0, 0, values1), (0, 0, values2) ]

  """
    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        #super(TomCatSaleOrder, self).onchange_sale_order_template_id()
        if not self.sale_order_template_id:
            self.require_signature = self._get_default_require_signature()
            self.require_payment = self._get_default_require_payment()
            return
        template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)

        order_lines = [(5, 0, 0)]
        for line in template.sale_order_template_line_ids:
            data = self._compute_line_data_for_template_change(line)
            if line.product_id:
                discount = 0
                if self.pricelist_id:
                    price = self.pricelist_id.with_context(uom=line.product_uom_id.id).get_product_price(line.product_id, 1, False)
                    if self.pricelist_id.discount_policy == 'without_discount' and line.price_unit:
                        discount = (line.price_unit - price) / line.price_unit * 100
                        # negative discounts (= surcharge) are included in the display price
                        if discount < 0:
                            discount = 0
                        else:
                            price = line.price_unit
                    elif line.price_unit:
                        price = line.price_unit

                else:
                    price = line.price_unit

                data.update({
                    'price_unit': price,
                    'project':line.project,
                    'ubication':line.ubication,
                    'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                    'product_uom_qty': line.product_uom_qty,
                    'product_id': line.product_id.id,
                    'product_uom': line.product_uom_id.id,
                    'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                })
                if self.pricelist_id:
                    data.update(self.env['sale.order.line']._get_purchase_price(self.pricelist_id, line.product_id, line.product_uom_id, fields.Date.context_today(self)))
            order_lines.append((0, 0, data))

        self.order_line = order_lines
        self.order_line._compute_tax_id()

        option_lines = [(5, 0, 0)]
        for option in template.sale_order_template_option_ids:
            data = self._compute_option_data_for_template_change(option)
            option_lines.append((0, 0, data))
        self.sale_order_option_ids = option_lines

        if template.number_of_days > 0:
            self.validity_date = fields.Date.to_string(datetime.now() + timedelta(template.number_of_days))

        self.require_signature = template.require_signature
        self.require_payment = template.require_payment

        if template.note:
            self.note = template.note
        #Original override
        for item in  self.order_line:
             item.product_uom_change()
        


    def search_proyects(self,doc):
    
        actual_proy = doc.order_line[0].project_sections.name if doc.order_line[0].display_type == 'line_project' else "Sin proyecto asignado"
        actual_index = 0
        item = [actual_proy, [] ]
        items = [item]
        
        for prod in  doc.order_line[1:] if actual_proy != "Sin proyecto asignado"   else doc.order_line:
            if prod.display_type == 'line_project':
                actual_index+=1 
                items.append([prod.project_sections.name, [] ])
            else:

                items[actual_index][1].append(prod)
 
        return items
    def generate_discount(self):
        if self.order_line:
          
            view_id = self.env.ref('tomcat.view_sale_discount_wizard').id
            view = {
                'name': ('Descuento'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'tomcat.sale.discount.wizard',
                'views':  [(view_id,'form')],
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context':{'default_sale':self.id}
                
       
           
            
        }
        return view 
    def generate_report_v2(self,sale):    
        ids = sale.order_line.ids
        items = self.env['sale.order.line'].search([('id','in',ids)], order='project asc, ubication asc ,name asc ')
        tree = []
        items = items.filtered(lambda x: x.product_id.type != 'service' and x.product_id.service_tracking != 'project_only' )
        for key, group in itertools.groupby(items, key=lambda x:(  x['project'] ) ):
            item = {
                'project':key.name,
                'ubications':self.ubication_product(group)

            }
            item['total'] = sum([ubi['total'] for ubi in item['ubications'] ])
            tree.append(item)
        return tree
    
    def ubication_product(self,group_t):
        ubications = []
        for key, group in itertools.groupby(group_t, key=lambda x:( x['ubication'] ) ):
            items =  [item for item in group]
            item= { 
                    'ubication':key.name,
                    'items':items,
                    'total':sum([prod.price_subtotal for prod in items ])
            }
            ubications.append(item)

        return ubications
    def export_xls(self, data, token):
        jdata = json.loads(data)
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet("titulo")
        header_bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")
        header_plain = xlwt.easyxf("pattern: pattern solid, fore_colour gray25;")
        bold = xlwt.easyxf("font: bold on;")

        measure_count = jdata['measure_count']
        origin_count = jdata['origin_count']

        # Step 1: writing col group headers
        col_group_headers = jdata['col_group_headers']

        # x,y: current coordinates
        # carry: queue containing cell information when a cell has a >= 2 height
        #      and the drawing code needs to add empty cells below
        x, y, carry = 1, 0, deque()
        for i, header_row in enumerate(col_group_headers):
            worksheet.write(i, 0, '', header_plain)
            for header in header_row:
                while (carry and carry[0]['x'] == x):
                    cell = carry.popleft()
                    for j in range(measure_count * (2 * origin_count - 1)):
                        worksheet.write(y, x+j, '', header_plain)
                    if cell['height'] > 1:
                        carry.append({'x': x, 'height': cell['height'] - 1})
                    x = x + measure_count * (2 * origin_count - 1)
                for j in range(header['width']):
                    worksheet.write(y, x + j, header['title'] if j == 0 else '', header_plain)
                if header['height'] > 1:
                    carry.append({'x': x, 'height': header['height'] - 1})
                x = x + header['width']
            while (carry and carry[0]['x'] == x):
                cell = carry.popleft()
                for j in range(measure_count * (2 * origin_count - 1)):
                    worksheet.write(y, x+j, '', header_plain)
                if cell['height'] > 1:
                    carry.append({'x': x, 'height': cell['height'] - 1})
                x = x + measure_count * (2 * origin_count - 1)
            x, y = 1, y + 1

        # Step 2: writing measure headers
        measure_headers = jdata['measure_headers']

        if measure_headers:
            worksheet.write(y, 0, '', header_plain)
            for measure in measure_headers:
                style = header_bold if measure['is_bold'] else header_plain
                worksheet.write(y, x, measure['title'], style)
                for i in range(1, 2 * origin_count - 1):
                    worksheet.write(y, x+i, '', header_plain)
                x = x + (2 * origin_count - 1)
            x, y = 1, y + 1

        # Step 3: writing origin headers
        origin_headers = jdata['origin_headers']

        if origin_headers:
            worksheet.write(y, 0, '', header_plain)
            for origin in origin_headers:
                style = header_bold if origin['is_bold'] else header_plain
                worksheet.write(y, x, origin['title'], style)
                x = x + 1
            y = y + 1

        # Step 4: writing data
        x = 0
        for row in jdata['rows']:
            worksheet.write(y, x, row['indent'] * '     ' + ustr(row['title']), header_plain)
            for cell in row['values']:
                x = x + 1
                if cell.get('is_bold', False):
                    worksheet.write(y, x, cell['value'], bold)
                else:
                    worksheet.write(y, x, cell['value'])
            x, y = 0, y + 1

        response = request.make_response(None,
            headers=[('Content-Type', 'application/vnd.ms-excel'),
                    ('Content-Disposition', 'attachment; filename=table.xls')],
            cookies={'fileToken': token})
        workbook.save(response.stream)

        return response
    def action_quotation_send(self):
        values = super(TomCatSaleOrder, self).action_quotation_send()
        ctx = values['context']
        
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('Testing')
        worksheet.write_merge(0 , 0,  2, 5, "Cliente")
        fp =  BytesIO()
        workbook.save(fp)
        
        Attachment = self.env['ir.attachment']
        attachment_ids = []    
        data_attach = {
                'name': "cotz.xls",
                'datas': base64.encodestring( fp.getvalue()) ,
                'res_model': 'mail.compose.message',
                'res_id': 0,
                'type': 'binary',  # override default_type from context, possibly meant for another model!
        }
        attachment_ids.append(Attachment.create(data_attach).id)
        
        ctx['default_excel'] = True
        ctx['default_attachment_ids'] = [(6, 0, attachment_ids) ]
        values['context'] = ctx 
        return values 



class SaleReport(models.Model):
    _inherit = "sale.report"

    proyect = fields.Many2one('project.project', string='Proyecto',track_visibility=True,required=True)
    
    name_proy = fields.Char('Name proyect', readonly=True)

class MailComposerTomcat(models.TransientModel):
    _inherit = 'mail.compose.message'
    excel = fields.Boolean('Excel',default=False)
    """
    @api.onchange('excel')
    def on_change_excel(self):
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('Testing')
        worksheet.write_merge(0 , 0,  2, 5, "Cliente")
        fp =  BytesIO()
        workbook.save(fp)
        values = {}
        values['attachment_ids'] =  [(0, 0,  
                                      { 
                                        'name': "cotz.xls",
                                        'store_fname':"cotz.xls",
                                        'datas':base64.encodestring(fp.getvalue()) 
                                      }
                                                                      ) ]
        values = self._convert_to_write(values)
        return {'value': values}
    """

    """
    @api.onchange('excel')
    def on_change_excel(self):
                workbook = xlwt.Workbook(encoding='utf-8')
                worksheet = workbook.add_sheet('Testing')
                worksheet.write_merge(0 , 0,  2, 5, "Cliente")
                fp =  BytesIO()
                workbook.save(fp)
                values = {}
                attachment_ids = []
                Attachment = self.env['ir.attachment']
            
                data_attach = {
                        'name': "cotz.xls",
                        'datas': base64.encodestring( fp.getvalue()) ,
                        'res_model': 'mail.compose.message',
                        'res_id': 0,
                        'type': 'binary',  # override default_type from context, possibly meant for another model!
                }
                attachment_ids.append(Attachment.create(data_attach).id)
                values['attachment_ids'] = [(6, 0, attachment_ids) ]
                values = self._convert_to_write(values)
                return {'value': values}
    """
    @api.onchange('template_id')
    def onchange_template_id_dos(self):
                workbook = xlwt.Workbook(encoding='utf-8')
                worksheet = workbook.add_sheet('Testing')
                worksheet.write_merge(0 , 0,  2, 5, "Cliente")
                fp =  BytesIO()
                workbook.save(fp)
                values = {}
                attachment_ids = []
                Attachment = self.env['ir.attachment']
            
                data_attach = {
                        'name': "cotz.xls",
                        'datas': base64.encodestring( fp.getvalue()) ,
                        'res_model': 'mail.compose.message',
                        'res_id': 0,
                        'type': 'binary',  # override default_type from context, possibly meant for another model!
                }
                attachment_ids.append(Attachment.create(data_attach).id)
                values['attachment_ids'] = [(6, 0, attachment_ids) ]
                values = self._convert_to_write(values)
                return {'value': values}