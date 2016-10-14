from openerp import models, fields, api, _
from openerp.exceptions import except_orm
from openerp.osv import osv
import urllib2, httplib, urlparse, gzip, requests, json
from StringIO import StringIO
import openerp.addons.decimal_precision as dp
from datetime import date
import logging
import ast
#Get the logger
_logger = logging.getLogger(__name__)

class order_recommendation_lines(models.TransientModel):
	_name = 'order.recommendation.line'

	@api.one
	def _compute_rule_explanation(self):
		return_value = ''
		if self.rule_recommended:
			return_value = 'Cada vez que se compra el producto ' + self.product_id.name + '\n'
			return_value = 'se compra tambien el/los productos '
			for rule in self.rule_recommended.rhr.ids:
				product_name = self.env['product.product'].browse(rule).name
				return_value = return_value + product_name + ','
			return_value = return_value + ' un ' + str(self.rule_recommended.confidence*100) + '% de veces'
		self.rule_explanation = return_value

	recommendation_id = fields.Many2one('order.recommendation')
	product_id = fields.Many2one('product.product',string='Product')
	rule_recommended = fields.Many2one('product.association.rule')
	rule_explanation = fields.Char('Explicacion',compute=_compute_rule_explanation)


class order_recommendation(models.TransientModel):
        _name = 'order.recommendation'

	order_id = fields.Many2one('sale.order')
	recommendation_lines = fields.One2many(comodel_name='order.recommendation.line',inverse_name='recommendation_id')	



