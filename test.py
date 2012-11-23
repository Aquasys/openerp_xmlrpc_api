#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
# Aquasys G.K.

# Copyright (C) 20012-2013.

#

# This program is free software: you can redistribute it and/or modify

# it under the terms of the GNU Affero General Public License as

# published by the Free Software Foundation, either version 3 of the

# License, or (at your option) any later version.

#

# This program is distributed in the hope that it will be useful,

# but WITHOUT ANY WARRANTY; without even the implied warranty of

# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the

# GNU Affero General Public License for more details.

#

# You should have received a copy of the GNU Affero General Public License

# along with this program. If not, see <http://www.gnu.org/licenses/>.
#########################################################################
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
