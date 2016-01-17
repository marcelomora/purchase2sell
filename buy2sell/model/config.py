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
        'host':fields.char('Host', 255, help='Another database host'),
        'username':fields.char('Username', 255
            , help='Username for sale order creation'),
        'password':fields.char('Password', 255, help='Password'),
        'database':fields.char('Database', 255, help='Database'),
        'default':fields.boolean('Default', help='Default configuration'),
        'state':fields.selection([('draft', 'Draft'), ('confirm', 'Confirm')],
            string='State', help='State'),

    }

    _defaults = {
        'state' : 'draft',
    }

    def action_test_conn(self, cr, uid, ids, context=None):
        config_obj = self.browse(cr, uid, ids, context)
        config = config_obj[0]
        try:
            client = Client(config.host, db=config.database, user=config.username,
                    password=config.password)
            return self.write(cr, uid, ids, {'state':'confirm'}, context=context)
        except Exception, e:
            raise osv.except_osv((_("Error")), (e))




