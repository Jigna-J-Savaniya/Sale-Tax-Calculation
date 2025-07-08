from odoo import api, fields, models, _
from collections import defaultdict


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tax_summary_ids = fields.One2many('consolidate.tax', 'order_id', string="Tax Summary ids")

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        self.tax_summary_ids.unlink()
        summary = defaultdict(float)
        for line in self.order_line:
            taxes = line.tax_id.compute_all(
                price_unit=line.price_unit,
                currency=self.currency_id,
                quantity=line.product_uom_qty,
                product=line.product_id,
                partner=self.partner_id,
            )
            for tax in taxes.get('taxes', []):
                tax_name = self.env['account.tax'].browse(tax['id']).tax_group_id.name
                tax_amount = tax['amount']
                summary[tax_name] += tax_amount

        # Create summary records
        for name, amt in summary.items():
            self.env['consolidate.tax'].create({
                'order_id': self.id,
                'tax_name': name,
                'amount': amt,
            })
        return res


class ConsolidateTax(models.Model):
    _name = 'consolidate.tax'

    order_id = fields.Many2one('sale.order')
    amount = fields.Float('Total Tax Amount')
    tax_name = fields.Char(string='Tax')
