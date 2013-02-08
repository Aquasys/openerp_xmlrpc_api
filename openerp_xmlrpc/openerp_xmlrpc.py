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
import xmlrpclib
import base64


class OpenerpXmlRpc():
    def __init__(self, protocol='https', host='localhost', port='8069',
                 context={}, **kwargs):
        """
        init method for class

        :param protocol: http or https
        :param host: ip or domain or the OpenERP server
        :param port: port number on OpenERP server is running
        :param context: context is a session variable for OpenERP Language
                        control,default value set will be done with this
        context={'lang':'jp_JP'}

        """
        # object connection to call object methods
        self.object_connection = xmlrpclib.ServerProxy(
            "%s://%s:%s/xmlrpc/object" % (protocol, host, port))
        #database connection to utilize databse functionality
        self.db_connection = xmlrpclib.ServerProxy(
            "%s://%s:%s/xmlrpc/db" % (protocol, host, port))
        #common connection to call common methods like login
        self.common_connection = xmlrpclib.ServerProxy(
            "%s://%s:%s/xmlrpc/common" % (protocol, host, port))
        #report connection to call report methods like report, report_get
        self.report_connection = xmlrpclib.ServerProxy(
            "%s://%s:%s/xmlrpc/report" % (protocol, host, port))
        #seting up class variables
        self.uid = False
        self.port = port
        self.host = host
        self.protocol = protocol
        self.context = context

    def login(self, database='demo', user_name='admin', password='admin'):
        """
        Function to call OpenERP Login Method

        :param database: Database name of OpenERP
        :param user_name: user name of OpenERP for provided database
        :param password: password of user name for provided database

        :return: integer User Id for the session
        """
        try:

            #authenticating
            self.uid = self.common_connection.login(database, user_name,
                                                    password)
            #setup Database and Password in class variable
            self.database = database
            self.password = password

            return self.uid

        except Exception as excep:
            raise excep

    def db_list(self):
        """ Fuction which returns Database list from OpenERP """

        try:
            #retrieving list of database(s)
            return self.db_connection.list()
        except Exception as excep:
            raise excep

    def search(self, oerp_object, domain=[], offset=0, limit=False,
               order=False, context=False, count=False):
        """
        Function to search OpenERP records on basis on Criteria

        :param oerp_object: OpenERP object name e.g res.partner of partner,
                            sale.order for Sales
        :param args: list of tuples specifying the search domain
                     [('field_name', 'operator', value), ...].
                     Pass an empty list to match all records.
        :param offset: optional number of results to skip in the returned
                       values (default: 0)
        :param limit: optional max number of records to
                      return (default: **None**)
        :param order: optional columns to sort by (default: self._order=id )
        :param context: optional context arguments, like lang, time zone
        :type context: dictionary
        :param count: optional (default: **False**), if **True**,
                      returns only the number of records matching the criteria,
                      not their ids

        :return: id or list of ids of records matching the criteria
        """
        try:
            #calling search method of OpenERP
            return self.execute(oerp_object, 'search', domain, offset, limit,
                                order, context, count)
        except Exception as excep:
            raise excep

    def read(self, oerp_object, ids, fields=[], context={}):
        """
        Function to read existing record(s) of OpenERP based on Id

        :param oerp_object: OpenERP object name e.g res.partner of partner,
                            sale.order for Sales
        :param ids: id or list of the ids of the records to read
        :param fields: optional list of field names to
                       return (default: all fields would be returned)
        :type fields: list (example ['field_name_1', ...])
        :param context: optional context dictionary - it may
                        contains keys for specifying certain options
                        like ``context_lang``, ``context_tz`` to alter the
                        results of the call. A special ``bin_size`` boolean
                        flag may also be passed in the context to request the
                        value of all fields.binary columns to be returned as
                        the size of the binary instead of its contents.
                        This can also be selectively overridden by passing a
                        field-specific flag in the form ``bin_size_XXX:
                        True/False`` where ``XXX`` is the name of the field.
                        Note: The ``bin_size_XXX`` form is new in OpenERP v6.0.
        :return: list of dictionaries((dictionary per record asked)) with
                 requested field values
        """
        try:
            #calling read method of OpenERP
            return self.execute(oerp_object, 'read', ids, fields, context)
        except Exception as excep:
            raise excep

    def write(self, oerp_object, ids, vals, context={}):
        """
        Function to Write values in Existing OpenERP record

        :param oerp_object: OpenERP object name e.g res.partner of partner,
                            sale.order for Sales
        :param ids: object id or list of object ids to update according to
                    **vals**
        :param vals: field values to update,
                     e.g {'field_name': new_field_value, ...}
        :type vals: dictionary
        :param context: (optional) context arguments,
                        e.g. {'lang': 'en_us', 'tz': 'UTC', ...}
        :type context: dictionary
        :return: True
        """
        try:
            if not isinstance(ids, (list, tuple)):
                ids = [ids]
            #calling write method of OpenERP
            return self.execute(oerp_object, 'write', ids, vals, context)
        except Exception as excep:
            raise excep

    def create(self, oerp_object, vals, context={}):
        """
        Function to create new record in OpenERP

        :param oerp_object: OpenERP object name e.g res.partner of partner,
                            sale.order for Sales
        :param vals: field values for new record,
                     e.g {'field_name': field_value, ...}
        :type vals: dictionary
        :param context: optional context arguments,
                        e.g. {'lang': 'en_us', 'tz': 'UTC', ...}
        :type context: dictionary
        :return: id of new record created
        """
        try:
            #calling create method of OpenERP
            return self.execute(oerp_object, 'create', vals, context)
        except Exception as excep:
            raise excep

    def unlink(self, oerp_object, ids, context={}):
        """
        Function to delete existing record in OpenERP

        :param ids: id or list of ids
        :param context: (optional) context arguments, like lang, time zone
        :return: True
        """
        try:
            if not isinstance(ids, (list, tuple)):
                ids = [ids]
            return self.execute(oerp_object, 'unlink', ids, context)

        except Exception as excep:
            raise excep

    def fields_get(self, oerp_object, fields=[], context={},
                   write_access=True):
        """
        Function to get field(s) properties

        :param fields: list of fields
        :param context: context arguments, like lang, time zone
        :return: dictionary of field dictionaries, each one describing a
                 field of the business object
        """
        try:
            return self.execute(oerp_object, 'fields_get', fields, context,
                                write_access)
        except Exception as excep:
            raise excep

    def execute(self, oerp_object, method, *arg):
        """
        Execute any method at OpenERP side with existing OpenERP objects

        :param oerp_object: OpenERP object name e.g res.partner of partner,
                            sale.order for Sales
        :param: method: Any valid OpenERP method (even Custom Added Methods can
                        be called)
        """

        #calling method based on ``method`` variable value
        try:
            return self.object_connection.execute(self.database, self.uid,
                                                  self.password,
                                                  oerp_object, method, *arg)
        except Exception as excep:
            raise excep

    def report(self, report_name, ids, report_type='pdf', context={}):
        result = False

        if not isinstance(ids, (list, tuple)):
            ids = [ids]

        report_id = self.report_connection.report(
            self.database, self.uid, self.password, report_name,
            ids, {'report_type': report_type}
        )
        status = False
        res_val = {}
        while not status:
            res_val = self.report_connection.report_get(
                self.database, self.uid, self.password, report_id)
            status = res_val['state']

        result = res_val.get('result', False)
        if result:
            result = base64.decodestring(result)

        return result

if __name__ == '__main__':
    #context variable
    context = {'lang': 'ja_JP'}

    #initializing Connection
    oerp = OpenerpXmlRpc(port=8079, )

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
