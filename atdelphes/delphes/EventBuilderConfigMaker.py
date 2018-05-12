# Tai Sakuma <tai.sakuma@gmail.com>
import os
import logging

import ROOT

from alphatwirl.roottree.inspect import is_ROOT_null_pointer

from .DelphesEvents import DelphesEvents
from .load_delphes import load_delphes

##__________________________________________________________________||
class EventBuilderConfigMaker(object):
    def __init__(self, check_files=True, skip_error_files=True):
        self.check_files = check_files
        self.skip_error_files = skip_error_files

        self.tree_name = 'Delphes'

    def __repr__(self):
        name_value_pairs = (
            ('check_files', self.check_files),
            ('skip_error_files', self.skip_error_files),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def create_config_for(self, dataset, files, start, length):
        config = dict(
            events_class=DelphesEvents,
            file_paths=files,
            tree_name=self.tree_name,
            max_events=length,
            start=start,
            check_files=self.check_files,
            skip_error_files=self.skip_error_files,
            dataset=dataset, # for scribblers
            name=dataset.name # for the progress report writer
        )
        return config

    def file_list_in(self, dataset, maxFiles=-1):
        if maxFiles < 0:
            return dataset.files
        return dataset.files[:min(maxFiles, len(dataset.files))]

    def nevents_in_file(self, path):
        load_delphes()
        file_ = ROOT.TFile.Open(path)
        if is_ROOT_null_pointer(file_) or file_.IsZombie():
            logger = logging.getLogger(__name__)
            if self.skip_error_files:
                logger.warning('cannot open {}'.format(path))
                return 0
            logger.error('cannot open {}'.format(path))
            raise OSError('cannot open {}'.format(path))
        tree = file_.Get(self.tree_name)
        return tree.GetEntriesFast()

##__________________________________________________________________||
