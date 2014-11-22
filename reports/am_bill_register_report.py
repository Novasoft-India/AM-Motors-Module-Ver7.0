from openerp import tools
from openerp.osv import fields, osv

class am_bill_register_report(osv.osv):
    """
         Open ERP Model for AMMOTORS Bill Register Report
    """
    _name = 'am.bill.register.report'
    _description = 'am.bill.register.report'
    _auto = False
 
    _columns = {
            'number':fields.char('Invoice',size=64,readonly=True),
            'state':fields.char('State',size=64,readonly=True),
            'date_invoice': fields.date('Invoice Date', readonly=True),
            'vechile_model_id':fields.many2one('ammotors.vechilemodel','Model',readonly=True),
            'executive_id':fields.many2one('hr.employee','Executive',readonly=True),
            'deliver_branch_id':fields.many2one('ammotors.branch','Branch',readonly=True),
            'chase_no':fields.char('Chasis No',size=64,readonly=True),
            'delivery_date': fields.date('Delivery Date', readonly=True),
            'amount_untaxed': fields.float('Taxable Amount', readonly=True),  
            'vat_amt': fields.float('Vat ', readonly=True),
            'vat_1_amt': fields.float('CVat ', readonly=True),
            'st_12amt': fields.float('Service Tax', readonly=True),
            'st_1_12amt': fields.float('CService Tax', readonly=True),
            'edushe': fields.float('Educational Cess', readonly=True),             
            'amount_tax' : fields.float('Tax Total',readonly=True),
            'amount_total' : fields.float('Bill Amount',readonly=True)
            }
    _order = 'number'
    
    
    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'am_bill_register_report')
        cr.execute("""          
                CREATE OR REPLACE VIEW am_bill_register_report AS( 
                   SELECT 
                    min(a_i.id) as id,
                    a_i.create_date, 
                    a_i.number, 
                    a_i.amount_tax, 
                    a_i.state, 
                    a_i.date_invoice, 
                    a_i.amount_untaxed, 
                    a_i.amount_total, 
                    a_i_vat.amount as vat_amt,
                    a_i_vat1.amount as vat_1_amt, 
                    a_i_st.amount as  st_12amt,
                    a_i_st1.amount as  st_1_12amt,
                    a_i_she.amount as  edushe,
                    s_o.vechile_model_id, 
                    s_o.deliver_branch_id, 
                    s_o.chase_no, 
                    s_o.executive_id, 
                    s_o.delivery_date                    
                FROM 
                    account_invoice a_i
                    left join account_invoice_tax a_i_vat on (a_i.id= a_i_vat.invoice_id) AND a_i_vat.name = 'VAT 14.5'
                    left join account_invoice_tax a_i_vat1 on (a_i.id= a_i_vat1.invoice_id) AND a_i_vat1.name = 'VAT14.5%'
                    left join account_invoice_tax a_i_st on (a_i.id= a_i_st.invoice_id) AND a_i_st.name = 'ST 12%' 
                    left join account_invoice_tax a_i_st1 on (a_i.id= a_i_st1.invoice_id) AND a_i_st1.name = 'ST@12%'
                    left join account_invoice_tax a_i_she on (a_i.id= a_i_she.invoice_id) AND a_i_she.name = 'Edu. SHE  3%'                     
                    left join sale_order s_o on (s_o.id=a_i.x_so)                     
                Group By                    
                    a_i.create_date, 
                    a_i.number, 
                    a_i.amount_tax, 
                    a_i.state, 
                    a_i.date_invoice, 
                    a_i.amount_untaxed, 
                    a_i.amount_total,                   
                    a_i_vat.amount ,
                    a_i_vat1.amount , 
                    a_i_st.amount , 
                    a_i_st1.amount ,
                    a_i_she.amount , 
                    s_o.vechile_model_id, 
                    s_o.deliver_branch_id, 
                    s_o.chase_no, 
                    s_o.executive_id, 
                    s_o.delivery_date                                     
                    )
                    """)
    
am_bill_register_report()
