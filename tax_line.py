from openerp.osv import osv
from openerp.osv import fields

class am_account_tax(osv.osv):
    """
         Open ERP Model
    """
    _inherit = 'account.tax' 
    
    _description = 'adding base_percentage field for base tax calculation Modification'
 
    _columns = {
            'base_percentage':fields.float('Base Percentage', required=True),
        }
am_account_tax()