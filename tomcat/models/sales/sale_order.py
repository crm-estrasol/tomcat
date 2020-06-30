# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from datetime import datetime
from dateutil.relativedelta import relativedelta

from datetime import timedelta, datetime, date
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

from PIL import Image
import os.path

class TomCatSaleOrder(models.Model):
    _inherit  = "sale.order"
    proyect = fields.Many2one('project.project', string='Proyecto',track_visibility=True)
    product_proy = fields.Many2one('product.product', string='Plantilla proyecto',track_visibility=True, domain="['&',('type', '=', 'service'),('service_tracking', '=', 'project_only')]", readonly=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    name_proy = fields.Char('Nombre proyecto',track_visibility=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    print_options = fields.Selection([('complete_total', 'Completo  totalizado'), 
                                                ('only_complete', 'Completo') , ('complete_price', 'Completo con precio unitario'), ('no_brandModel','Sin marca y modelo') ,
                                                ('without_price', 'Sin precios'),('subtotal_system', 'Solo con subtotal por sistema')], string='Formato pdf', copy=False, default='only_complete')
    client_model = fields.Boolean( string='Modelo cliente')
    excel = fields.Boolean( string='Formato excel')
    partner_avaible =   fields.Many2many(related="user_id.partner_avaible")
    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True, change_default=True, index=True, tracking=1,
        domain="['&','|', ('company_id', '=', False), ('company_id', '=', company_id),('id', 'in', partner_avaible)]",)
    porcent = fields.Monetary(compute='_product_porcent', help="Total descuento.", currency_field='currency_id', store=True)
    margin_porcent = fields.Float(compute='_margin_porcent', help="Margen %.",digits=(16, 2) ,store=True)
    #Add proyect item
    @api.model
    def create(self, values): 
        res = super(TomCatSaleOrder, self).create(values)
        if  res.name_proy :
            res.write({'name':res.name+"-"+res.name_proy})
        if  'product_proy' in values:  
            product = self.env['product.product'].search( [ ('id','=', values['product_proy'])] )
            res.order_line =  [ (0,0 ,{'product_id':product.id,'name':product.name,'product_uom':product.uom_id.id}) ]
        return res
   #Redefine log
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

    #Inlcude concet section
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
   #inherit and set maring
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
    #WIZARD
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
                     'total':sum([prod.price_unit for prod in items ])
                    #'total':sum([prod.price_subtotal for prod in items ])
            }
            ubications.append(item)

        return ubications
    def current_date(self):
        return datetime.today().strftime('%d/%m/%Y')
   
    def action_quotation_send(self):
        values = super(TomCatSaleOrder, self).action_quotation_send()
        ctx = values['context']
        
        #workbook = xlwt.Workbook(encoding='utf-8')
        #worksheet = workbook.add_sheet('Testing')
        #worksheet.write_merge(0 , 0,  2, 5, "Cliente")
        #fp =  BytesIO()
        #workbook.save(fp)
        
        #Attachment = self.env['ir.attachment']
        #attachment_ids = []    
        #data_attach = {
        #        'name': "cotz.xls",
        #        'datas': base64.encodestring( fp.getvalue()) ,
        #        'res_model': 'mail.compose.message',
        #        'res_id': 0,
        #        'type': 'binary',  # override default_type from context, possibly meant for another model!
        #}
        #attachment_ids.append(Attachment.create(data_attach).id)
        
        ctx['default_excel'] = True if self.excel else False
        #ctx['default_attachment_ids'] = [(6, 0, attachment_ids) ]
        values['context'] = ctx 
        return values 
    #excel
    def get_order_data(self):
        ids = self.order_line.ids
        items = self.env['sale.order.line'].search([('id','in',ids)] , order='project asc, ubication asc ,name asc ')
        items = items.filtered(lambda x: x.product_id.type != 'service' and x.product_id.service_tracking != 'project_only' )
        return items 

    @api.onchange('user_id')
    def on_user_id(self):
        self.partner_id = False 
        self.partner_invoice_id = False
        self.partner_shipping_id = False

  
    
    @api.depends('order_line.margin','order_line.price_subtotal')
    def _product_porcent(self):
        for order in self:
            total = 0
            
            for order_line in order.order_line:
                if  order_line.discount > 0 and order_line.price_subtotal > 0 :
                    disct =  order_line.discount/100
                    discount_real = 1 - disct
                    orginal = order_line.price_subtotal / discount_real    
                    total += orginal - order_line.price_subtotal


                else:
                    total += 0    
            order.porcent = total 
    @api.depends('order_line.margin','order_line.price_subtotal')
    def _margin_porcent(self):
        for order in self:
            order.margin_porcent = ( order.margin * 100 ) / order.amount_untaxed  if order.amount_untaxed != 0 else 0 
class SaleReport(models.Model):
    _inherit = "sale.report"

    proyect = fields.Many2one('project.project', string='Proyecto',track_visibility=True,required=True)
    
    name_proy = fields.Char('Name proyect', readonly=True)

class MailComposerTomcat(models.TransientModel):
    _inherit = 'mail.compose.message'
    excel = fields.Boolean('Excel',default=False)
    external_document =  fields.Boolean('Cotización externa', default=False)
    purchase =  fields.Boolean('Purchase flag', default=False)
   

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
    def onchange_template_id_wrapper(self):
        super(MailComposerTomcat, self).onchange_template_id_wrapper()
        if self.excel:
            self.excel_format()
        if  self.purchase and  self.external_document:
             setattr(self, 'attachment_ids', [(6, 0, [] ) ])    
    
           
    def excel_format(self):
        data = self.env['sale.order'].search( [('id','=',self.res_id)] )
        order_data = data.get_order_data()
        fp  = self.create_book(data,order_data)
        values = {}
        attachment_ids = []
        Attachment = self.env['ir.attachment']     
        data_attach = {
                'name': data.name+'.xls',
                'datas': base64.encodestring( fp.getvalue()) ,
                'res_model': 'mail.compose.message',
                'res_id': 0,
                'type': 'binary', 
        }
        attachment_ids.append(Attachment.create(data_attach).id)
        values['attachment_ids'] = [(6, 0, attachment_ids) ]
        values = self._convert_to_write(values)
        #Attch + xls
        setattr(self, 'attachment_ids', [(6, 0, [x.id for x in self.attachment_ids] + attachment_ids) ])
    
    def create_book(self,data, order_data):
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet(data.name)
        #COLORS 
        xlwt.add_palette_colour("low_white_t", 0x21)
        
        workbook.set_colour_RGB(0x21, 222, 234, 246)
        #COLORS 
        #MODEDA
        currency_style = xlwt.XFStyle()
        currency_style.num_format_str = "[$$-409]#,##0.00;-[$$-409]#,##0.00"
        #MODEDA
        #---------STYLES
        no_border = """borders: top_color white, bottom_color white, right_color white, left_color white,
                                    left thin, right thin, top thin, bottom thin;"""
        border = """borders: top_color black, bottom_color black, right_color black, left_color black,
                                    left thin, right thin, top thin, bottom thin;"""
        header_bold = xlwt.easyxf("""
                                    font: bold on; pattern: pattern solid, fore_colour white; align: vert center, horz center ,wrap on;
                                    """+no_border)
        header_blue = xlwt.easyxf(" font: bold on, height 230; pattern: pattern solid, fore_colour low_white_t; align:  vert center, horz center ,wrap on;"+border)
        bHeader_blue = xlwt.easyxf(" font: bold on, height 230; pattern: pattern solid, fore_colour low_white_t;  align: horz center;"+border) 
        font_blue = xlwt.easyxf("font: colour  blue;"+no_border)
        text_cell = xlwt.easyxf("font:  height 230;   align: wrap on ; "+no_border)
        ctext_cell =  xlwt.easyxf("font:  height 230; align: horz center;"+no_border)
        c2text_cell =  xlwt.easyxf("font:  height 230; align: vert center, horz center ,wrap on;"+border)
        c2bText_cell =  xlwt.easyxf("font:  height 230 ,bold on; align: vert center, horz center ;"+border)
        c2text_cellMoney = xlwt.easyxf("font:  height 230 ; align: vert center, horz center ;"+border)
        c2text_cellMoney.num_format_str = "[$$-409]#,##0.00;-[$$-409]#,##0.00"
        line = xlwt.easyxf( """borders: top_color white, bottom_color black, right_color white, left_color white,
                                    left thin, right thin, top thin, bottom thin;""")
        text_cellLast = xlwt.easyxf("font:  height 230;   align: vert center, horz center, wrap on ; ")
        #---------STYLES
        #--- adjust columns
        #worksheet.write_merge(6, 6, 3, 3,'Pass')
     
        first_col = worksheet.col(0)
        first_col.width = 256 * 7 #characters 
        
        second_col = worksheet.col(1)
        second_col.width = 256 * 30 #characters 
        
        adjust_total =  worksheet.col(7)
        adjust_total.width = 256 * 14 #characters 
        
        worksheet.row(10).height_mismatch = True
        row_table = worksheet.row(10)
        row_table.height = 200 * 1 #characters 
        worksheet.row(12).height_mismatch = True
        row_col = worksheet.row(12)
        row_col.height = 256 * 2 #characters 
        #--- adjust columns        
        
        
        #IMAGEN
        
        #script_dir = os.path.dirname(os.path.abspath('colocaralcentro.png'))
        #im = os.path.join(script_dir, 'colocaralcentro.png')    
        img = Image.open('/home/odoo/src/user/tomcat/static/src/img/150x150.png')
        r, g, b, a = img.split()
        img = Image.merge("RGB", (r, g, b))
        #img.thumbnail((154,154), Image.ANTIALIAS)
        img = img.save('colocarcentro.bmp')
        
        worksheet.insert_bitmap('colocarcentro.bmp', 0,0,50,0)
        worksheet.merge(0,8,0,1)
        #IMAGEN



        #Company_info
        worksheet.write_merge(0 , 0,  2, 5, self.env.user.company_id.name,header_bold)
        worksheet.write_merge(1 , 1,  2, 5,  self.env.user.company_id.phone,font_blue )
        T =  self.env.user.company_id.website
        L = 'http://'+ self.env.user.company_id.website
        formula = 'HYPERLINK("{}", "{}")'.format(L, T)
        worksheet.write_merge(2 , 2,  2, 5, xlwt.Formula(formula),font_blue )
        T = data.user_id.email
        formula = 'mailto:{}'.format(T)
        worksheet.write_merge(3 , 3,  2, 5, formula,font_blue )
        address =  "{} {} {} {} {} {}" .format(self.env.user.company_id.street,self.env.user.company_id.street_number2, self.env.user.company_id.street2,self.env.user.company_id.city, self.env.user.company_id.state_id.name,self.env.user.company_id.country_id.name )
        item_size =  len(address)
        if item_size > 30:
                worksheet.row(4).height_mismatch = True
                row_col = worksheet.row(4)
                size = int( (item_size / 30) + 1 ) 
                row_col.height = 300 * size #characters 
        worksheet.write_merge(4 , 4,  2, 5, address,text_cell)
        worksheet.write_merge(5 , 5,  2, 5, "CP: "+str(self.env.user.company_id.zip ),text_cell)
        worksheet.write_merge(6 , 6,  2, 5, "RFC: "+str(self.env.user.company_id.vat),text_cell)
        worksheet.write_merge(7 , 7,  2, 5, "Régimen Fiscal: "+str(self.env.user.company_id.company_registry),text_cell)
        #Company_info
        today = date.today()
        # dd/mm/YY
        d1 = today.strftime("%d/%m/%Y")
      
        #Customer infor
        worksheet.write_merge(0 , 0,  6, 10, "Numero Cotización",header_blue )
        worksheet.write_merge(1 , 1,  6, 10, data.name,c2text_cell )
        worksheet.write_merge(2 , 2,  6, 10, "Fecha",header_blue )
        worksheet.write_merge(3 , 3,  6, 10, d1,c2text_cell )
        worksheet.write_merge(4 , 4,  6, 10, "EMPRESA",header_blue )
        worksheet.write_merge(5 , 5,  6, 10, data.partner_id.parent_id.name if data.partner_id.parent_id else data.partner_id.name ,c2text_cell )
        worksheet.write_merge(6 , 6,  6, 10, "Contacto",header_blue )
        worksheet.write_merge(7 , 7,  6, 10, data.partner_id.name,c2text_cell )
        #Customer infor
                
        worksheet.write_merge(9 , 9,  0, 1, "PROYECTO",header_blue )
        worksheet.write_merge(9 , 9,  2, 10, data.name_proy,c2text_cell )

        worksheet.write_merge(11 , 11,  0, 10, "DETALLE COTIZACIÓN",bHeader_blue )
        
        worksheet.write(12 , 0,"Partida",c2bText_cell)
        worksheet.write(12 , 1, "Sistema",c2bText_cell )
        worksheet.write(12 , 2, "Ubicación",c2bText_cell )
        worksheet.write(12 , 3, "Marca",c2bText_cell )
        worksheet.write(12 , 4, "Modelo",c2bText_cell )
        worksheet.write_merge(12, 12,  5, 7, "Descripción",c2bText_cell )
        worksheet.write(12 , 8, "Cantidad",c2bText_cell )
        worksheet.write(12 , 9, "P. unitario",c2bText_cell )
        worksheet.write(12 , 10, "P. total",c2bText_cell )
        actual_row = 13
        current_count =1    
        
        for item in order_data:
            worksheet.write(actual_row , 0, current_count,c2text_cell)
            worksheet.write(actual_row , 1, item.project.name ,c2text_cell )
            worksheet.write(actual_row , 2, item.ubication.name,c2text_cell )
            worksheet.write(actual_row , 3, item.product_id.brand.name,c2text_cell )
            worksheet.write(actual_row , 4, item.product_id.name,c2text_cell )
            worksheet.write_merge(actual_row, actual_row,  5, 7, item.name,c2text_cell )
            #Ajustar tamaño renglon 
            worksheet.write(actual_row , 8, item.product_uom_qty ,c2text_cell )
            #Pendiente formato precios
            worksheet.write(actual_row , 9, item.price_unit,c2text_cellMoney  )
            worksheet.write(actual_row , 10, item.price_subtotal,c2text_cellMoney  )
            item_size =  len(item.name)
            if item_size > 19:
                worksheet.row(actual_row).height_mismatch = True
                row_col = worksheet.row(actual_row)
                size = int( (item_size / 20) + 1 ) 
                row_col.height = 300 * size #characters 
            actual_row+=1
            current_count+=1
        
        actual_row+=1
        worksheet.write_merge(actual_row , actual_row,  0, 5, "OBSERVACIONES",bHeader_blue )
        worksheet.write(actual_row , 6, "Moneda",bHeader_blue )
        worksheet.write(actual_row , 7, "",bHeader_blue )
        worksheet.write_merge(actual_row , actual_row,  8, 10, "Total",bHeader_blue )
        
        actual_row+=1
        worksheet.write_merge(actual_row , actual_row+3,  0, 5, "Descripción", c2text_cell)
        worksheet.write_merge(actual_row , actual_row+3,  6, 6, data.currency_id.name, c2text_cell)
        
        worksheet.write(actual_row , 7, "SUB TOTAL",c2text_cell )
        worksheet.write_merge(actual_row ,actual_row ,  8, 10, data.amount_untaxed,c2text_cellMoney )
        
        worksheet.write(actual_row+1 , 7, "DESCUENTO",c2text_cell )
        worksheet.write_merge(actual_row+1 ,actual_row+1 ,  8, 10, data.porcent,c2text_cellMoney )

        worksheet.write(actual_row+2 , 7, "IVA 16%",c2text_cell )
        worksheet.write_merge(actual_row+2 ,actual_row+2 ,  8, 10, data.amount_tax,c2text_cellMoney )
        
        worksheet.write(actual_row+3 , 7, "TOTAL",c2text_cell )
        worksheet.write_merge(actual_row+3 ,actual_row+3 ,  8, 10, data.amount_total,c2text_cellMoney )
       
       
        #
        
        actual_row +=5    
        worksheet.write( actual_row, 0, "NOTAS", c2bText_cell )

        
        quaranty = [
                    "GARANTÍA DE INSTALACIÓN 1 AÑO ",
                    "GARANTÍA DE LOS EQUIPOS DE 1 A 3 AÑOS ",
                    "GARANTÍA EN PROGRAMACIÓN DE POR VIDA ",
                    "ALMACENAMIENTO Y SEGURO DE EQUIPO PREVIO A INSTALACIÓN INCLUIDO",
                    "SEGURO DE RESPONSABILIDAD CIVIL POR $3 MILLONES DE PESOS ",
                    "PUEDE SER PAGADO EN DÓLARES AMERICANOS POR TRANSFERENCIA ELECTRÓNICA O EN MONEDA NACIONAL AL TIPO DE CAMBIO DE VENTA DEL BANCO BANORTE",
                    "EN ESTA PROPUESTA NO SE CONSIDERA OBRA CIVIL",
                    "ESTA COTIZACIÓN EXPIRA EN {}".format( data.validity_date.strftime("%d/%m/%Y") ) 

                    ]
        actual_row+=1                
        for msg in quaranty:
            worksheet.write_merge(actual_row , actual_row,  0, 8,msg ,text_cell)
            actual_row+=1  
        actual_row+=2
        worksheet.write_merge(actual_row , actual_row,  0, 5,"Condiciones de pago" ,c2bText_cell)
        actual_row+=1
        worksheet.write_merge(actual_row , actual_row,  0, 5,data.payment_term_id.name ,text_cell)
        actual_row+=2
        worksheet.write_merge(actual_row , actual_row,  0, 5,"Notas" ,c2bText_cell)
        actual_row+=1
        worksheet.write_merge(actual_row , actual_row,  0, 5,data.note ,text_cell)

        item_size =  len(data.note)
        if item_size > 19:
                worksheet.row(actual_row).height_mismatch = True
                row_col = worksheet.row(actual_row)
                size = int( (item_size / 70) + 1 ) 
                row_col.height = 300 * size #characters
        
        actual_row+=3
        worksheet.write_merge(actual_row , actual_row,  3, 8,  "",line)
        actual_row+=1
        worksheet.write_merge(actual_row , actual_row,  3, 8,"ING."+data.user_id.name ,text_cellLast)
        



        #worksheet.write(actual_row+2 , 10, "TOTAL",c2text_cell )



        
        
        
        
        fp =  BytesIO()
        workbook.save(fp)
       
        return fp