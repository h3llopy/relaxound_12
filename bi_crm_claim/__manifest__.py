# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'CRM Claim Management',
    'version': '12.0.0.2',
    'category': 'Sales',
    'author': "Techspawn",
    'website': 'www.techspawn.com',
    'sequence': 5,
    'summary': 'This plugin helps to manage after sales services as claim management',
    'description': "Claim system for your product, claim management, submit claim, claim form, Ticket claim, support ticket, issue, website project issue, crm management, ticket handling,support management, project support, crm support, online support management, online claim, claim product, claim services, issue claim, fix claim, raise ticket, raise issue, view claim, display claim, list claim on website ",
    'license':'OPL-1',
    'depends': ['base','crm','sale','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_claim_menu.xml',
        'views/crm_claim_data.xml',
        'views/res_partner_view.xml',
        'views/crm_claim_tag_view.xml',
        'report/claim_report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    "images":["static/description/Banner.png"],
}
