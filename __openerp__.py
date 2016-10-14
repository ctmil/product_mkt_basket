{
    'name': 'Productos - Reglas de Asociacion',
    'category': 'Sales',
    'version': '0.1',
    'depends': ['base','product','sale'],
    'data': [
	#'security/ir.model.access.csv',
	#'security/security.xml',
	#'wizard/wizard_view.xml',
	'product_view.xml',
	'wizard/wizard_view.xml',
    ],
    'demo': [
    ],
    'qweb': [],
    'installable': True,
}
