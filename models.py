from openerp import models, fields, api, _
from openerp.osv import osv
from openerp.exceptions import except_orm, ValidationError
from StringIO import StringIO
import urllib2, httplib, urlparse, gzip, requests, json
import openerp.addons.decimal_precision as dp
import logging
import datetime
from openerp.fields import Date as newdate
from datetime import datetime, timedelta
from dateutil import relativedelta
#Get the logger
_logger = logging.getLogger(__name__)


class product_association_rule(models.Model):
	_name = 'product.association.rule'
	_description = 'Reglas de asociacion de productos'

	name = fields.Char('Nombre',required=True)
	product_id = fields.Many2one('product.product',string='Producto')
	lhr = fields.Many2many(comodel_name='product.product',relation='lhr_product_association',\
				column1='lhr_product_1',column2='lhr_product_2',string='Producto regla izquierda')
	rhr = fields.Many2many(comodel_name='product.product',relation='rhr_product_association',\
				column1='rhr_product_1',column2='rhr_product_2',string='Producto regla derecha')
	support = fields.Float(string='Soporte')
	confidence = fields.Float(string='Confianza')
	lift = fields.Float(string='Lift')

class product_product(models.Model):
	_inherit = 'product.product'

	association_rule_ids = fields.One2many(comodel_name='product.association.rule',inverse_name='product_id')
