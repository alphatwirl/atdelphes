hasROOT = False
try:
    import ROOT
    hasROOT = True
except ImportError:
    pass

if hasROOT:
    from .DelphesEvents import DelphesEvents
    from .EventBuilderConfigMaker import EventBuilderConfigMaker
    from .build import BuildDelphesEvents

    # deprecated
    from .DelphesEventBuilder import DelphesEventBuilder
