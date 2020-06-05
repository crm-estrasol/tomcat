# -*- coding: utf-8 -*-
{
    'name': "TomCat",

    'summary': """
        New features Odoo""",

    'description': """
        Inherit some views , new vies , reports
    """,

    'author': "Estrasol -Kevin Daniel del Campo",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','mrp','sale','stock',
                'account','sale_margin','sale_management',
                'contacts','product','mail','web','crm',
                'sale_crm','stock','project','hr_timesheet',
                'purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/user/user.xml',
        'views/theme/res_config_settings_views.xml',   
        'views/theme/theme.xml',
        'views/contact/contact.xml',
        'views/contact/intermediary_category.xml',
        'views/contact/customer_segment.xml',
        'views/contact/menu.xml',
        'views/crm/crm.xml',
        'views/crm/crm_cron.xml',
        'views/mail/mail_activity.xml',
        'views/project/project.xml',
        'views/sales/sales.xml',
        'views/sales/product_template.xml',
        'views/sales/extra_cat_product/product_brand.xml',
        'views/sales/extra_cat_product/product_project.xml',
        'views/sales/extra_cat_product/product_ubication.xml',
        'views/purchase/purchase.xml',
          # 'views/sales/sale_order_line.xml',
        
        'views/templates/templates.xml',
        
        #'views/sales/sales_cron.xml',
        #'views/portal/sale/sale_order.xml',
        
        'reports/sales_report_only_system.xml',
        'reports/sales_report_without_price.xml',
        'reports/sales_report_no_brand_model.xml',
        'reports/sales_report_total.xml',
        'reports/sales_report_complete_total.xml',
        'reports/sales_report_price_unit.xml',
        'reports/sales_report.xml',
        'reports/excel.xml',
        'reports/purchase/purchase_report_document.xml',
        'reports/purchase/purchasequotation_report_document.xml',
         
        
        'reports/sale_report_prueba.xml', 

        'reports/reports.xml',
        'wizard/sale_details.xml',
        
        'mail/mail_report.xml',
        #'views/menus/menus.xml',
    ],  
     'qweb': [
          'qweb/replace_menu_base.xml',
         ]
        ,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
