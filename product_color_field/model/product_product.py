# # -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.osv import expression

class product_product(models.Model):
    _inherit = "product.product"

    @api.multi
    def name_get(self):
        def _name_get(d):
            name = d.get('name', '')
            code = self._context.get('display_default_code', True) and d.get('default_code', False) or False
            color = d.get('color', False)
            if code:
                name = '[%s] %s' % (code, name)
            if color:
                name = '%s (%s)' % (name, color)
            return d['id'], name

        partner_id = self._context.get('partner_id')
        if partner_id:
            partner_ids = [partner_id, self.env['res.partner'].browse(partner_id).commercial_partner_id.id]
        else:
            partner_ids = []

        # all user don't have access to seller and partner
        # check access asubscriptablend use superuser
        self.check_access_rights("read")
        self.check_access_rule("read")

        result = []

        self.sudo().read(['name', 'default_code', 'product_tmpl_id', 'attribute_value_ids', 'attribute_line_ids'],
                         load=False)

        product_template_ids = self.sudo().mapped('product_tmpl_id').ids

        if partner_ids:
            supplier_info = self.env['product.supplierinfo'].sudo().search([
                ('product_tmpl_id', 'in', product_template_ids),
                ('name', 'in', partner_ids),
            ])
            # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
            # Use `load=False` to not call `name_get` for the `product_tmpl_id` and `product_id`
            supplier_info.sudo().read(['product_tmpl_id', 'product_id', 'product_name', 'product_code'], load=False)
            supplier_info_by_template = {}
            for r in supplier_info:
                supplier_info_by_template.setdefault(r.product_tmpl_id, []).append(r)
        for product in self.sudo():
            # display only the attributes with multiple possible values on the template
            variable_attributes = product.attribute_line_ids.filtered(lambda l: len(l.value_ids) > 1).mapped(
                'attribute_id')
            variant = product.attribute_value_ids._variant_name(variable_attributes)

            name = variant and "%s (%s)" % (product.name, variant) or product.name
            sellers = []
            if partner_ids:
                product_supplier_info = supplier_info_by_template.get(product.product_tmpl_id, [])
                sellers = [x for x in product_supplier_info if x.product_id and x.product_id == product]
                if not sellers:
                    sellers = [x for x in product_supplier_info if not x.product_id]
            if sellers:
                for s in sellers:
                    seller_variant = s.product_name and (
                            variant and "%s (%s)" % (s.product_name, variant) or s.product_name
                    ) or False
                    mydict = {
                        'id': product.id,
                        'name': seller_variant or name,
                        'default_code': s.product_code or product.default_code,
                        'color': product.color_id.name,
                    }
                    temp = _name_get(mydict)
                    if temp not in result:
                        result.append(temp)
            else:
                mydict = {
                    'id': product.id,
                    'name': name,
                    'default_code': product.default_code,
                    'color': product.color_id.name,
                }
                result.append(_name_get(mydict))
        return result

        # for product in self.browse(cr, SUPERUSER_ID, ids, context=context):
        # for product in self.browse(self):
        #     variant = ", ".join([v.name for v in product.attribute_value_ids])
        #     variant = False
        #     name = variant and "%s (%s)" % (product.name, variant) or product.name
        #     sellers = []
        #     if partner_ids:
        #         sellers = [x for x in product.seller_ids if (x.name.id in partner_ids) and (x.product_id == product)]
        #         if not sellers:
        #             sellers = [x for x in product.seller_ids if (x.name.id in partner_ids) and not x.product_id]
        #     if sellers:
        #         for s in sellers:
        #             seller_variant = s.product_name and (
        #                     variant and "%s (%s)" % (s.product_name, variant) or s.product_name
        #             ) or False
        #             mydict = {
        #                 'id': product.id,
        #                 'name': seller_variant or name,
        #                 'default_code': s.product_code or product.default_code,
        #                 'color': product.color_id.name,
        #             }
        #             temp = _name_get(mydict)
        #             if temp not in result:
        #                 result.append(temp)
        #     else:
        #         mydict = {
        #             'id': product.id,
        #             'name': name,
        #             'default_code': product.default_code,
        #             'color': product.color_id.name,
        #         }
        #         result.append(_name_get(mydict))
        # return result
