# REVERSE
@property
def _rev_event_(self):
    elt = self.db.table('collorg.event.event')
    elt._task_ = self
    return elt

