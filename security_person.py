from openerp.osv import osv, fields
from datetime import datetime, timedelta

class security_person(osv.Model):
    _name = "hotel.security.person"

    def action_draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'draft'}, context=context)
    
    def action_confirm(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'confirmed'}, context=context)
    
    def action_void(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'void'}, context=context)
    
    _columns = {
                'security_person_id' : fields.char(string="Personel Note Number", size=256, required=True, states={'draft':[('readonly', False)]}, help=''),
                'in_datetime' : fields.datetime(string="Incoming Date Time", states={'draft':[('readonly', False)]}, help=''),
                'out_datetime' : fields.datetime(string="Outgoing Date Time", states={'draft':[('readonly', False)]}, help=''),
                'spk': fields.text('SPK', size=30, readonly=True, states={'draft':[('readonly', False)]}),
                'tools': fields.text('Tools', readonly=True, states={'draft':[('readonly', False)]}),  
                'person_detail': fields.one2many('hotel.security.person.detail', 'security_person_id','Person Detail', readonly=True, states={'draft':[('readonly', False)]}),                              

                'photo1': fields.binary('Photo 1', readonly=True, states={'draft':[('readonly', False)]}),
                'photo2': fields.binary('Photo 2', readonly=True, states={'draft':[('readonly', False)]}),
                
                'user': fields.many2one('res.users', 'On Duty', select=True, readonly=True),
                'state' : fields.selection([('draft','Draft'),
                                            ('confirmed','Confirmed'),
                                            ('void','Void')], string="State", states={'draft':[('readonly', False)]}, help=''),
                }
    
    _sql_constraints = [
        ('security_person_id_unique','UNIQUE(security_parking_id)','Security Parking ID is used!'),            
    ]
    
    _defaults = {
         'in_datetime' : fields.datetime.now,
         'out_datetime' : fields.datetime.now,
         'security_person_id': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'hotel.security.person'),
         'user': lambda obj, cr, uid, context: uid,
         'state': 'draft'
    }
    
    
class security_person_detail(osv.Model):
    _name = "hotel.security.person.detail"

    _columns = {
                'security_person_id': fields.many2one('hotel.security.person', 'Person Note ID', required=True, ondelete='cascade', select=True, readonly=True, states={'draft':[('readonly',False)]}),
                'personname' : fields.char(string="Person Name", size=100, required=True, states={'draft':[('readonly', False)]}, help=''),
                'personid' : fields.char(string="Person ID (KTP)", size=25, required=True, states={'draft':[('readonly', False)]}, help=''),
               }
    
#    _defaults = {
#         'personname': lambda obj, cr, uid, context: uid,
#         'personid': lambda obj, cr, uid, context: uid,
#    }    