
from odoo import fields, models
class ResPartner(models.Model):
    _inherit = 'res.partner'

    fraudulent_ids = fields.Many2many(
    'fraudulent.fraudulent',
    string="fraudulent Teams")