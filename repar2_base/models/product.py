# -*- coding: utf-8 -*-
from odoo import api, fields, models
from os.path import dirname, join, realpath
import csv


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    def publish_on_all_websites(self):
        self.sudo().write({'company_id': False})


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _cron_update_variants(self):
        csv_path = join(dirname(realpath(__file__)).replace('/models', ''), 'data', 'product.product.csv')
        vals_dict = {}
        vals = {}

        with open(csv_path, 'r') as csv_file:
            for row in csv.reader(csv_file, delimiter=','):
                if row[2] and row[3]:
                    if row[0]:
                        vals = {'default_code': row[0], 'product_tmpl_id': row[1],
                                'values': [row[2]], 'attributes': [row[3]]}
                        vals_dict[row[0]] = vals
                    else:
                        vals['values'].append(row[2])
                        vals['attributes'].append(row[3])

        for key, value in vals_dict.items():
            try:
                attributes = [self.env.ref(x) for x in value.get('attributes')]
                values = [self.env.ref(x) for x in value.get('values')]
                products = self.search([('product_tmpl_id', '=', self.env.ref(value.get('product_tmpl_id')).id)])
                if products:
                    product = products.filtered(lambda v: all(
                        (attribute_value.product_attribute_value_id in values) and
                        (attribute_value.attribute_id in attributes)
                        for attribute_value in v.product_template_attribute_value_ids))
                    if product:
                        name = value.get('name')
                        currency = value.get('currency_id')
                        product.write({'default_code': key})
            except Exception as e:
                print(e.args)
                import ipdb; ipdb.set_trace()

        print('ààààààààààààààààààààààààààààààààààààààààààààà')
