import os

from datapackage_pipelines.utilities.lib_test_helpers import (
    mock_processor_test
)

import datapackage_pipelines_ukds.processors
from .test_utils import TestBase

import logging
log = logging.getLogger(__name__)

ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')


class TestAddOAIMetadataProcessor(TestBase):

    def test_add_oai_metadata_processor(self):

        # input arguments used by our mock `ingest`
        datapackage = {
            'name': 'my-datapackage',
            'resources': []
        }
        params = {
            'oai_url': 'http://reshare.ukdataservice.ac.uk/cgi/oai2',
            'oai_id': '851500'
        }

        # Path to the processor we want to test
        processor_dir = \
            os.path.dirname(datapackage_pipelines_ukds.processors.__file__)
        processor_path = os.path.join(processor_dir, 'add_oai_metadata.py')

        # Trigger the processor with our mock `ingest` and capture what it will
        # returned to `spew`.
        spew_args, _ = mock_processor_test(processor_path,
                                           (params, datapackage, []))

        spew_dp = spew_args[0]

        # Asserts for the datapackage
        expected_dp = {
            'name': 'my-datapackage',
            'resources': [],
            'title': 'Farm Management Survey- SPSS data set',
            'description': 'A description of the data set...',
            'contributors': [{'title': 'Winter, Michael', 'role': 'author'}],
            'homepage': 'http://reshare.ukdataservice.ac.uk/851500/',
            'keywords': ['Environment, conservation and land use', 'History', 'Economics', 'Industry and management'],  # noqa
            'publisher': 'UK Data Archive',
            'sources': [{'title': 'RES-062-23-1831 SPSS data handbook.xlsx', 'path': 'http://reshare.ukdataservice.ac.uk/851500/1/RES-062-23-1831%20SPSS%20data%20handbook.xlsx'}, {'title': 'RES-062-23-1831 FBS data for ESRC archive.sav', 'path': 'http://reshare.ukdataservice.ac.uk/851500/2/RES-062-23-1831%20FBS%20data%20for%20ESRC%20archive.sav'}, {'title': 'http://reshare.ukdataservice.ac.uk/851500/3/nofile/', 'path': 'http://reshare.ukdataservice.ac.uk/851500/3/nofile/'}, {'title': 'unknown://notapath', 'path': 'unknown://notapath'}]  # noqa
        }
        self.assertEqual(spew_dp, expected_dp)
