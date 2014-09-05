from openerp.osv import osv, fields
from datetime import datetime, timedelta

class security_mail(osv.Model):
    _name = "hotel.security.mail"

    def action_draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'draft'}, context=context)
    
    def action_confirm(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'confirmed'}, context=context)
    
    def action_received(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'received'}, context=context)

    def action_void(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'void'}, context=context)
    
    _columns = {
                'security_mail_id' : fields.char(string="Mail Note Number", size=256, required=True, states={'draft':[('readonly', False)]}, help=''),
                'in_datetime' : fields.datetime(string="Incoming Date Time", states={'draft':[('readonly', False)]}, help=''),
                'mail_note': fields.text("Mail Note", states={'draft':[('readonly', False)]}, help=''),
                'mail_detail': fields.one2many('hotel.security.mail.detail', 'security_mail_id','Mail Detail', readonly=True, states={'draft':[('readonly', False)]}),                              

                'user': fields.many2one('res.users', 'On Duty', select=True, readonly=True),
                'state' : fields.selection([('draft','Draft'),
                                            ('confirmed','Confirmed'),
                                            ('received','Received'),
                                            ('void','Void')], string="State", states={'draft':[('readonly', False)]}, help=''),
                }
    
    _sql_constraints = [
        ('security_mail_id_unique','UNIQUE(security_mail_id)','Security Mail ID is used!'),            
    ]
    
    _defaults = {
         'in_datetime' : fields.datetime.now,
         'security_mail_id': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'hotel.mail.person'),
         'user': lambda obj, cr, uid, context: uid,
         'state': 'draft'
    }
    
    
class security_mail_detail(osv.Model):
    _name = "hotel.security.mail.detail"

    _columns = {
                'security_mail_id': fields.many2one('hotel.security.mail', 'Mail Note ID', required=True, ondelete='cascade', select=True, readonly=True, states={'draft':[('readonly',False)]}),
                'sender' : fields.char(string="Sender", size=100, required=True, states={'draft':[('readonly', False)]}, help=''),
                'receiver' : fields.char(string="Receiver", size=100, required=True, states={'draft':[('readonly', False)]}, help=''),
                'mail_no' : fields.char(string="Mail Number", size=25, required=True, states={'draft':[('readonly', False)]}, help=''),
               }

#    _defaults = {
#         'personname': lambda obj, cr, uid, context: uid,
#         'personid': lambda obj, cr, uid, context: uid,
#    }    