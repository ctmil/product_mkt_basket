#!/usr/bin/python
# -*- coding: utf-8 -*-


import xmlrpclib
import ssl
import csv

username = 'admin' #the user
pwd = 'admin'      #the password of the user
dbname = 'demo_sucursales'    #the database

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

f = open('rules.csv', 'rt')

reader = csv.reader(f)
nindex = 0
for row in reader:
        print row
        print nindex
	if nindex > 0:
		row = row[0]
		row = row.replace('\"','')
		row = row.replace('}','')
		row = row.replace('{','')
		lista = row.split('|')
		support = float(lista[2])
		confidence = float(lista[3])
		lift = float(lista[4])
		rules = lista[1].split('=>')
		lst_vals = []
		vals = {
			'name': lista[1],
			'support': support,
			'confidence': confidence,
			'lift': lift,
			}
		rule_index = 0
		insert_rule = False
		lst_lh_product_ids = []
		for rule in rules:
			rule = rule.strip()
			if rule != '' and rule_index == 0:
				a_rules = rule.split('#')
				insert_rule = True
				lst_lh_product_ids = []
				for a_rule in a_rules:
					lh_product_id = sock.execute(dbname,uid,pwd,'product.product','search',[('default_code','=',a_rule)])
				 	if lh_product_id:
						lst_lh_product_ids.append(lh_product_id[0])
			if rule != '' and rule_index > 0:
				a_rules = rule.split('#')
				insert_rule = True
				lst_rh_product_ids = []
				for a_rule in a_rules:
					rh_product_id = sock.execute(dbname,uid,pwd,'product.product','search',[('default_code','=',a_rule)])
				 	if rh_product_id:
						lst_rh_product_ids.append(rh_product_id[0])
			rule_index = rule_index + 1
		if insert_rule:
			if lst_lh_product_ids:
				for lh_product_id in lst_lh_product_ids:
					vals['product_id'] = lh_product_id
					vals['lhr'] = [(6,0,lst_lh_product_ids)]
					vals['rhr'] = [(6,0,lst_rh_product_ids)]
					return_id = sock.execute(dbname,uid,pwd,'product.association.rule','create',vals)
	nindex = nindex + 1
