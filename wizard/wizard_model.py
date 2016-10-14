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

	recommendation_id = fields.Many2one('order.recommendation')
	product_id = fields.Many2one('product.product',string='Product')
	rule_recommended = fields.Many2one('product.association.rule')


class order_recommendation(models.TransientModel):
        _name = 'order.recommendation'

	order_id = fields.Many2one('sale.order')
	recommendation_lines = fields.One2many(comodel_name='order.recommendation.line',inverse_name='recommendation_id')	



