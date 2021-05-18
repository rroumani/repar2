# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.template'

    def get_combinations_prices(self):
        self.ensure_one()

        combinations = self.env['product.template.attribute.value'].sudo()\
            .search([('product_tmpl_id', '=', self.id), ('price_extra', '>', 0)])\
            .sorted('price_extra', reverse=True)
        return combinations
