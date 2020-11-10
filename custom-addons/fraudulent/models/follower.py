from odoo import models, fields, api

class follower(models.Model):
    _inherit = 'res.partner'
    fraudulent_ids = fields.Many2many('fraudulent.fraudulent',string='fraudulent')

