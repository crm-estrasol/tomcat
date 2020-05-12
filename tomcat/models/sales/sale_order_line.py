# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from datetime import datetime
from dateutil.relativedelta import relativedelta

class TomPCatProjectSection(models.Model):
    _name = 'tomcat.project.section'
    _rec_name = 'name'
    name = fields.Char("Nombre")
  



class TomCatSaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    product_id = fields.Many2one(
        'product.product', string='Product', domain="[('sale_ok', '=', True),'&',('type', '!=', 'service'),('service_tracking', '!=', 'project_only'), '|', ('company_id', '=', False), ('company_id', '=', parent.company_id)]",
        change_default=True, ondelete='restrict', check_company=True)  # Unrequired company
    display_type = fields.Selection(selection_add=[('line_project', 'Proyecto')], default=False)
    
    
    project_sections = fields.Many2one('tomcat.project.section', string='Proyecto',track_visibility=True)
    type_proyect  = fields.Selection(related='product_id.service_tracking') 
    margin_tomcat =fields.Float("Margen %",  store=True, digits=(12, 2))
   

     
    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        valid_values = self.product_id.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids
        # remove the is_custom values that don't belong to this template
        for pacv in self.product_custom_attribute_value_ids:
            if pacv.custom_product_template_attribute_value_id not in valid_values:
                self.product_custom_attribute_value_ids -= pacv

        # remove the no_variant attributes that don't belong to this template
        for ptav in self.product_no_variant_attribute_value_ids:
            if ptav._origin not in valid_values:
                self.product_no_variant_attribute_value_ids -= ptav

        vals = {}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0

        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id, 
            margin_tomcat=self.product_id.margin_ut
           
        )
        vals['margin_tomcat'] = self.product_id.margin_ut
       
        vals.update(name=self.get_sale_order_line_multiline_description_sale(product))

        self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
          
            id_rule = self._get_display_rule(product)
            #value =  self.env['product.pricelist.item'].search([('id','=',id_rule)])[0]
            _logger.info("-----------------------------------"+str(id_rule) )
            #vals['margin_tomcat'] = value.margin_ut
            #vals['price_unit'] =  vals['price_unit']  / (1 -  vals['margin_tomcat'] ) 
            
          
        
        self.update(vals)

        title = False
        message = False
        result = {}
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s") % product.name
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            result = {'warning': warning}
            if product.sale_line_warn == 'block':
                self.product_id = False

        return result
    @api.onchange('product_id', 'price_unit', 'product_uom', 'product_uom_qty', 'tax_id')
    def _onchange_discount(self):

      
        if not (self.product_id and self.product_uom and
                self.order_id.partner_id and self.order_id.pricelist_id and
                self.order_id.pricelist_id.discount_policy == 'without_discount' and
                self.env.user.has_group('product.group_discount_per_so_line')):
            return

        self.discount = 0.0
        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id,
            quantity=self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id,
            fiscal_position=self.env.context.get('fiscal_position')
        )

        product_context = dict(self.env.context, partner_id=self.order_id.partner_id.id, date=self.order_id.date_order, uom=self.product_uom.id)

        price, rule_id = self.order_id.pricelist_id.with_context(product_context).get_product_price_rule(self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
        new_list_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id, self.product_uom_qty, self.product_uom, self.order_id.pricelist_id.id)

        if new_list_price != 0:
            if self.order_id.pricelist_id.currency_id != currency:
                # we need new_list_price in the same currency as price, which is in the SO's pricelist's currency
                new_list_price = currency._convert(
                    new_list_price, self.order_id.pricelist_id.currency_id,
                    self.order_id.company_id or self.env.company, self.order_id.date_order or fields.Date.today())
                
            discount = (new_list_price - price) / new_list_price * 100
            if (discount > 0 and new_list_price > 0) or (discount < 0 and new_list_price < 0):
                self.discount = discount
    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
            if not self.product_uom or not self.product_id:
                self.price_unit = 0.0
                return
            if self.order_id.pricelist_id and self.order_id.partner_id:
                product = self.product_id.with_context(
                    lang=self.order_id.partner_id.lang,
                    partner=self.order_id.partner_id,
                    quantity=self.product_uom_qty,
                    date=self.order_id.date_order,
                    pricelist=self.order_id.pricelist_id.id,
                    uom=self.product_uom.id,
                    fiscal_position=self.env.context.get('fiscal_position')
                )    
                self.price_unit = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id) 
                id_rule = self._get_display_rule(product)
                _logger.info("-----------------------------------"+str(id_rule) )
                value =  self.env['product.pricelist.item'].search([('id','=',id_rule)])[0]
                _logger.info("-----------------------------------"+str(id_rule) )
                #self.margin_tomcat = value.margin_ut
               # self.price_unit = self.price_unit  / (1 -  self.margin_tomcat[0].margin_ut ) 
    def _get_display_rule(self, product):
                # TO DO: move me in master/saas-16 on sale.order
                # awa: don't know if it's still the case since we need the "product_no_variant_attribute_value_ids" field now
                # to be able to compute the full price

                # it is possible that a no_variant attribute is still in a variant if
                # the type of the attribute has been changed after creation.
                no_variant_attributes_price_extra = [
                    ptav.price_extra for ptav in self.product_no_variant_attribute_value_ids.filtered(
                        lambda ptav:
                            ptav.price_extra and
                            ptav not in product.product_template_attribute_value_ids
                    )
                ]
                if no_variant_attributes_price_extra:
                    product = product.with_context(
                        no_variant_attributes_price_extra=tuple(no_variant_attributes_price_extra)
                    )

                if self.order_id.pricelist_id.discount_policy == 'with_discount':
                    return product.with_context(pricelist=self.order_id.pricelist_id.id).price
                product_context = dict(self.env.context, partner_id=self.order_id.partner_id.id, date=self.order_id.date_order, uom=self.product_uom.id)

                final_price, rule_id = self.order_id.pricelist_id.with_context(product_context).get_product_price_rule(self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
                _logger.info("-----------------------------------"+str(rule_id)+str(final_price) )
                return rule_id
    @api.onchange('margin_tomcat')
    def product_margin_ut(self):
       self.price_unit = self.price_unit  / (1 -  self.margin_tomcat ) 