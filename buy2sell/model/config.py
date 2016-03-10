# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from erppeek import Client

class buy2sell_config(osv.osv):
    _description="""
    Database access and configuration fields
    """
    _name="buy2sell.config"

    _columns={
        'name':fields.char('Name', 255, help='Conection name'),
        'provider_id':fields.many2one('res.partner', 'Provider',
            help='Set the provider for this configuration'),
        'customer_external_id':fields.char('Customer External Id',
            255, required=True, help='Customer External Id'),
        'customer_name':fields.char('Customer Name', 255,
            readonly = True, help='Customer Name'),
        'host':fields.char('Host', 255, help='Another database host',
            required=True),
        'username':fields.char('Username', 255, required=True,
            help='Username for sale order creation'),
        'password':fields.char('Password', 255, help='Password', required=True),
        'database':fields.char('Database', 255, help='Database', required=True),
        'supplier_id':fields.many2one('res.partner', 'Supplier',
            help='Provider', required=True, domain=[('supplier', '=', True)]),

        'state':fields.selection([('draft', 'Draft'),
                                  ('confirmed', 'Confirmed')],
            string='State', help='State'),
    }

    _defaults = {
        'state' : 'draft',
    }

    def action_test_conn(self, cr, uid, ids, context=None):
        config_obj = self.browse(cr, uid, ids, context)
        config = config_obj[0]
        vals = {'state':'draft'}
        try:
            client = Client(config.host, db=config.database, user=config.username,
                    password=config.password)
            model_data = client.model('ir.model.data')
            res_partner = client.model('res.partner')
            rows = model_data.browse(['model like partner'])\
                .read('complete_name res_id')
            for row in rows:
                if row['complete_name'] == config.customer_external_id:
                    customer_name = res_partner.browse(int(row['res_id'])).name
                    vals['customer_name'] = customer_name
                    vals['state'] = "confirmed"
                    break
            else:
                raise osv.except_osv((_("Error")), (_("Customer not found")))


            return self.write(cr, uid, ids, vals, context=context)
        except Exception, e:
            raise osv.except_osv((_("Error")), (e))




