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
    margin_tomcat = fields.Char("Nombre")
    marigin_tTotal  = fields.Char("Nombre")

     
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
            margin_tomcat="self.product_uom.id",
            marigin_tTotal="self.product_uom.id"
        )

        vals.update(name=self.get_sale_order_line_multiline_description_sale(product))

        self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
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
