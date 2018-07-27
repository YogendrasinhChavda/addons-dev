# -*- coding: utf-8 -*-
import datetime
from odoo import api, fields, models


class ReportSaleDetails(models.AbstractModel):

    _inherit = 'report.point_of_sale.report_saledetails'

    @api.model
    def get_sale_details(self, date_start=False, date_stop=False, configs=False):
        res = super(ReportSaleDetails, self).get_sale_details(date_start, date_stop, configs)

        expenses = self.env['hr.expense.sheet'].search([
            ('datetime', '>=', date_start),
            ('datetime', '<=', date_stop),
            ('state', '=', 'done')
        ])
        res['expenses_total'] = 0
        res['expenses'] = []
        for e in expenses:
            for line in e.expense_line_ids:
                data = {
                    'date': line.date,
                    'name': line.name,
                    'partner': line.employee_id.name,
                    'cashier': e.cashier,
                    'amount': line.total_amount*-1
                }
                res['expenses'].append(data)
                res['expenses_total'] = res['expenses_total'] + data['amount']
        return res
