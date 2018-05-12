# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

has_no_ROOT = False
try:
    import ROOT
except ImportError:
    has_no_ROOT = True

if not has_no_ROOT:
    from atdelphes.delphes import EventBuilderConfigMaker
    from atdelphes.delphes import DelphesEvents

##__________________________________________________________________||
pytestmark = pytest.mark.skipif(has_no_ROOT, reason="has no ROOT")

##__________________________________________________________________||
@pytest.fixture()
def mockroot(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['atdelphes.delphes.EventBuilderConfigMaker']
    monkeypatch.setattr(module, 'ROOT', ret)
    return ret

@pytest.fixture()
def mockdataset(monkeypatch):
    ret = mock.Mock()
    ret.name = 'TTJets'
    ret.files = ['/path/to/input1/tree.root', '/path/to/input2/tree.root']
    return ret

@pytest.fixture()
def mock_load_delphes(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['atdelphes.delphes.EventBuilderConfigMaker']
    monkeypatch.setattr(module, 'load_delphes', ret)
    return ret

@pytest.fixture()
def obj(mockroot, mock_load_delphes):
    return EventBuilderConfigMaker()

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_create_config_for(obj, mockdataset):
    expected = dict(
        events_class=DelphesEvents,
        file_paths=['/path/to/input1/tree.root', '/path/to/input2/tree.root'],
        tree_name='Delphes',
        max_events=30,
        start=20,
        dataset=mockdataset,
        name='TTJets',
        check_files=True,
        skip_error_files=True
    )
    actual = obj.create_config_for(
        dataset=mockdataset,
        files=['/path/to/input1/tree.root', '/path/to/input2/tree.root'],
        start=20,
        length=30
    )
    assert expected == actual

def test_file_list_in(obj, mockdataset):
    expected = ['/path/to/input1/tree.root', '/path/to/input2/tree.root']
    actual = obj.file_list_in(mockdataset)
    assert expected == actual

def test_file_list_in_maxFiles(obj, mockdataset):
    expected = [ ]
    actual = obj.file_list_in(mockdataset, maxFiles=0)
    assert expected == actual

##__________________________________________________________________||
@pytest.fixture()
def mocktfile():
    ret = mock.Mock()
    ret.good = True
    ret.IsZombie.return_value = False
    return ret

@pytest.fixture()
def mocktfile_null():
    ret = mock.Mock()
    ret.good = False
    ret.GetName.side_effect = ReferenceError
    return ret

@pytest.fixture()
def mocktfile_zombie():
    ret = mock.Mock()
    ret.good = False
    ret.IsZombie.return_value = True
    return ret

@pytest.fixture(params=['good', 'null', 'zombie'])
def file_(request, mocktfile, mocktfile_null, mocktfile_zombie):
    map_ = dict(good=mocktfile, null=mocktfile_null, zombie=mocktfile_zombie)
    return map_[request.param]

def test_nevents_in_file_skip(obj, file_, mockroot):
    obj.skip_error_files = True
    mockroot.TFile.Open.return_value = file_
    actual = obj.nevents_in_file(path='/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root')
    assert [mock.call.TFile.Open('/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root')] == mockroot.method_calls
    if file_.good:
        assert mockroot.TFile.Open().Get().GetEntriesFast() is actual
    else:
        assert 0 == actual

def test_nevents_in_file_raise(obj, file_, mockroot):
    obj.skip_error_files = False
    mockroot.TFile.Open.return_value = file_

    if not file_.good:
        with pytest.raises(OSError):
            actual = obj.nevents_in_file(path='/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root')
    else:
        actual = obj.nevents_in_file(path='/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root')

    assert [mock.call.TFile.Open('/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root')] == mockroot.method_calls

    if file_.good:
        assert mockroot.TFile.Open().Get().GetEntriesFast() is actual

##__________________________________________________________________||
