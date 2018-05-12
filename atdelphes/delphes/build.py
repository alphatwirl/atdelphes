# Tai Sakuma <tai.sakuma@gmail.com>
from alphatwirl.roottree import BuildEvents
from .load_delphes import load_delphes

##__________________________________________________________________||
class BuildDelphesEvents(BuildEvents):
    def __init__(self, config):
        super(BuildDelphesEvents, self).__init__(config)
    def __call__(self):
        load_delphes()
        return super(BuildDelphesEvents, self).__call__()

##__________________________________________________________________||
