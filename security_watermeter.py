from openerp.osv import osv, fields
from datetime import datetime, timedelta

class security_watermeter(osv.Model):
    _name = "hotel.security.watermeter"

    ''' def note_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'draft'})
        return True
    
    def note_confirm(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'confirm'})
        return True
    
    def note_void(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'void'})
        return True
    '''
    def action_draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'draft'}, context=context)
    
    def action_confirm(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'confirmed'}, context=context)
    
    def action_void(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'void'}, context=context)
    
    _columns = {
                'security_watermeter_id' : fields.char(string="Note Number", size=256, required=True, states={'draft':[('readonly', False)]}, help=''),
                'in_datetime' : fields.datetime(string="Incoming Date Time", states={'draft':[('readonly', False)]}, help=''),
                'meter_number' : fields.integer(string="Meter Number", states={'draft':[('readonly', False)]}, help=''),
                'photo1': fields.binary('Photo 1', readonly=True, states={'draft':[('readonly', False)]}),
                
                'user': fields.many2one('res.users', 'On Duty', select=True, readonly=True),
                'state' : fields.selection([('draft','Draft'),
                                            ('confirmed','Confirmed'),
                                            ('void','Void')], string="State", states={'draft':[('readonly', False)]}, help=''),
                }
    
    _sql_constraints = [
        ('security_watermeter_id_unique','UNIQUE(security_watermeter_id)','Security watermeter ID is used!'),            
    ]
    
    _defaults = {
         'in_datetime' : fields.datetime.now,
         'security_watermeter_id': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'hotel.security.watermeter'),
         'user': lambda obj, cr, uid, context: uid,
         'state': 'draft'
    }