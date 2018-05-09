# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

has_no_ROOT = False
try:
    import ROOT
except ImportError:
    has_no_ROOT = True

if not has_no_ROOT:
    from atdelphes.delphes import DelphesEvents

##__________________________________________________________________||
pytestmark = pytest.mark.skipif(has_no_ROOT, reason="has no ROOT")

##__________________________________________________________________||

##__________________________________________________________________||
