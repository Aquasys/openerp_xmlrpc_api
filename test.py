#!/usr/bin/env python
# -*- coding: utf-8 -*-
import openerp_xmlrpc

#context variable
context = {'lang': 'ja_JP'}

#initializing Connection
oerp = openerp_xmlrpc.OpenerpXmlRpc(port=8079, )

#getting db list
print oerp.db_list()

#login to OpenERP for Authentication
oerp.login(database='demo')

#searching example for partner
partner_ids = oerp.search('res.partner', [], context=context)

#reading example for partner based on search ids
partner_datas = oerp.read('res.partner', partner_ids[:12], ['name'],
                          context=context)
print partner_datas

#create example for partner
cr_id = oerp.create('res.partner', {'name': 'Grishma', 'code': 'GRS'},
                    context=context)
print cr_id

#write example for partner
res = oerp.write('res.partner', cr_id, {'name': 'Shukla'}, context=context)
print res

#calling valid mathod from execute direct
print oerp.execute('res.partner', 'name_get', cr_id, context)

#delete(unlink) example for partner
oerp.unlink('res.partner', cr_id, context=context)

#calling fields get for only name and code field
#Have a look by just passing language in context it will return String
#attribute in Jananish language
print oerp.fields_get('res.partner', ['name', 'code'], context)
#calling field get for all fields and without language
oerp.fields_get('res.partner', [])

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
