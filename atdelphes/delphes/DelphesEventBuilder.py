# Tai Sakuma <tai.sakuma@gmail.com>
from alphatwirl.roottree import EventBuilder

from .DelphesEvents import DelphesEvents
from .load_delphes import load_delphes

##__________________________________________________________________||
class DelphesEventBuilder(EventBuilder):
    def __init__(self, config):
        super(DelphesEventBuilder, self).__init__(config, EventsClass=DelphesEvents)
    def __call__(self):
        load_delphes()
        return super(DelphesEventBuilder, self).__call__()

##__________________________________________________________________||
