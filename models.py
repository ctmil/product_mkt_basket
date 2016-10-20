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

	@api.one
	def _compute_rule_text(self):
		lhr_products = []
		rhr_products = []
		for lhr_product_id in self.lhr.ids:
			lhr_products.append(self.env['product.product'].browse(lhr_product_id).name)
		for rhr_product_id in self.rhr.ids:
			rhr_products.append(self.env['product.product'].browse(rhr_product_id).name)
		if rhr_products:
			rhr_product_str = ','.join(rhr_products)
			lhr_product_str = ','.join(lhr_products)
			return_value = "Cada vez que se vende el/los producto/s %s tambien se vende el producto %s un %6.2f por ciento de veces"%\
				(lhr_product_str,rhr_product_str,self.confidence*100)
		self.rule_text = return_value

	name = fields.Char('Nombre',required=True)
	product_id = fields.Many2one('product.product',string='Producto')
	lhr = fields.Many2many(comodel_name='product.product',relation='lhr_product_association',\
				column1='lhr_product_1',column2='lhr_product_2',string='Producto regla izquierda')
	rhr = fields.Many2many(comodel_name='product.product',relation='rhr_product_association',\
				column1='rhr_product_1',column2='rhr_product_2',string='Producto regla derecha')
	support = fields.Float(string='Soporte')
	confidence = fields.Float(string='Confianza')
	lift = fields.Float(string='Lift')
	rule_text = fields.Char('Texto Recomendacion',compute=_compute_rule_text)

class product_product(models.Model):
	_inherit = 'product.product'

	association_rule_ids = fields.One2many(comodel_name='product.association.rule',inverse_name='product_id')

class sale_order(models.Model):
	_inherit = 'sale.order'

        @api.multi
        def order_recommendations(self):
                if self.state not in ['draft','sent']:
                        raise osv.except_osv(('Error'), ('Can create orders only in draft state'))
                        return None
		vals = {
			'order_id': self.id,
			}
		recommendation_id = self.env['order.recommendation'].create(vals)
		for line in self.order_line:
			if line.product_id.association_rule_ids:
				rule_ids = line.product_id.association_rule_ids
				for rule_id in rule_ids:
					vals_rule = {
						'recommendation_id': recommendation_id.id,
						'product_id': line.product_id.id,
						'rule_recommended': rule_id.id,
						}	
					rule_id = self.env['order.recommendation.line'].create(vals_rule)
                res = {
                        "name": "sale.order.recommendations"+str(self.id),
                        "type": "ir.actions.act_window",
                        "res_model": "order.recommendation",
                        "view_type": "form",
                        "view_mode": "form",
			"target": "new",
                        #"view_id": "product.product_supplierinfo_form_view",
                        "res_id": recommendation_id.id,
                        "nodestroy": True,
                        }
                return res

