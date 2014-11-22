from openerp import tools
from openerp.osv import fields, osv

class am_invoice_product_report(osv.osv):
    """
         Invoice Product REport Calculation
    """
    _name = 'am.invoice.product.report'
    _description = 'am.invoice.product.report'
    _auto = False
 
    _columns = {
            'origin':fields.char('Job Card',size=64,readonly=True),
            'state':fields.char('State',size=64,readonly=True),
            'date_invoice': fields.date('Invoice Date', readonly=True),
            'invoice_number':fields.char('Invoice No',size=64,readonly=True),
            'product_id':fields.many2one('product.product','Product',readonly=True),
            'categ_id':fields.many2one('product.category','Category',readonly=True),
            'type':fields.char('Type',size=64,readonly=True),
            'price_unit': fields.float('MRP', readonly=True),
            'quantity': fields.float('Quantity', readonly=True), 
            'price_subtotal': fields.float('Total', readonly=True),
            'price_margin': fields.float('Margin', readonly=True),           
            'name':fields.char('Name',size=64,readonly=True),
            'description':fields.char('Description',size=64,readonly=True)
            }
    _order = 'origin'
    
    
    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'am_invoice_product_report')
        cr.execute("""          
                CREATE OR REPLACE VIEW am_invoice_product_report AS( 
                select
                    min(inv_line.id) as id,
                    acc_inv.origin, 
                    acc_inv."number" AS invoice_number,
                    acc_inv.state, 
                    acc_inv.date_invoice, 
                    inv_line.product_id, 
                    inv_line.quantity, 
                    inv_line.price_subtotal, 
                    inv_line.price_unit, 
                    inv_line.name, 
                    p.name_template, 
                    p.price_margin, 
                    pt.description, 
                    pt.categ_id, 
                    pt.type   
                FROM 
                    account_invoice_line inv_line
                    join account_invoice acc_inv on (inv_line.invoice_id = acc_inv.id)
                    left join product_product p on (inv_line.product_id = p.id)
                    left join product_template pt on (pt.id=p.product_tmpl_id )
               GROUP BY
                    pt.categ_id,
                    acc_inv.origin,
                    acc_inv."number",
                    acc_inv.state,
                    acc_inv.date_invoice,
                    inv_line.product_id,
                    inv_line.quantity, 
                    inv_line.price_subtotal, 
                    inv_line.price_unit, 
                    inv_line.name, 
                    p.name_template, 
                    p.price_margin, 
                    pt.description, 
                    pt.categ_id, 
                    pt.type  
                    )
                    """)
    
am_invoice_product_report()