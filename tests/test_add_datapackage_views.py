import os

from datapackage_pipelines.utilities.lib_test_helpers import (
    mock_processor_test
)

import datapackage_pipelines_ukds.processors
from .test_utils import TestBase

import logging
log = logging.getLogger(__name__)

this_dir, this_filename = os.path.split(__file__)


class TestAddDatapackageViewsProcessor(TestBase):

    def test_add_datapackage_views_processor(self):

        # input arguments used by our mock `ingest`
        datapackage = {
            'name': 'my-datapackage',
            'resources': []
        }
        params = {
            'views': ['tests/sample_data/sample-view-spec.json']
        }

        # Path to the processor we want to test
        processor_dir = \
            os.path.dirname(datapackage_pipelines_ukds.processors.__file__)
        processor_path = os.path.join(processor_dir,
                                      'add_datapackage_views.py')

        # Trigger the processor with our mock `ingest` and capture what it will
        # returned to `spew`.
        spew_args, _ = mock_processor_test(processor_path,
                                           (params, datapackage, []))

        spew_dp = spew_args[0]

        # Asserts for the datapackage
        expected_dp = {
            'name': 'my-datapackage',
            'resources': [],
            'views': [
                {
                    'name': 'simple-view-bar',
                    'resources': ['my-resource'],
                    'spec': {'group': 'date', 'series': ['my-column'],
                             'type': 'bar'},
                    'specType': 'simple',
                    'title': 'My View Title'
                },
                {
                    'name': 'second-view',
                    'resources': ['my-resource'],
                    'spec': {'group': 'date', 'series': ['my-column'],
                             'type': 'bar'},
                    'specType': 'simple',
                    'title': 'My Second View Title'
                }
            ]
        }
        self.assertEqual(spew_dp, expected_dp)

    def test_add_datapackage_views_processor_existing_views(self):
        '''Adding views to datapackage that has existing views.'''

        # input arguments used by our mock `ingest`
        datapackage = {
            'name': 'my-datapackage',
            'resources': [],
            'views': [
                {
                    'name': 'existing-view',
                    'resources': ['my-resource'],
                    'spec': {'group': 'date', 'series': ['my-column'],
                             'type': 'bar'},
                    'specType': 'simple',
                    'title': 'My Existing View Title'
                }]
        }
        params = {
            'views': ['tests/sample_data/sample-view-spec.json']
        }

        # Path to the processor we want to test
        processor_dir = \
            os.path.dirname(datapackage_pipelines_ukds.processors.__file__)
        processor_path = os.path.join(processor_dir,
                                      'add_datapackage_views.py')

        # Trigger the processor with our mock `ingest` and capture what it will
        # returned to `spew`.
        spew_args, _ = mock_processor_test(processor_path,
                                           (params, datapackage, []))

        spew_dp = spew_args[0]

        # Asserts for the datapackage
        expected_dp = {
            'name': 'my-datapackage',
            'resources': [],
            'views': [
                {
                    'name': 'existing-view',
                    'resources': ['my-resource'],
                    'spec': {'group': 'date', 'series': ['my-column'],
                             'type': 'bar'},
                    'specType': 'simple',
                    'title': 'My Existing View Title'
                },
                {
                    'name': 'simple-view-bar',
                    'resources': ['my-resource'],
                    'spec': {'group': 'date', 'series': ['my-column'],
                             'type': 'bar'},
                    'specType': 'simple',
                    'title': 'My View Title'
                },
                {
                    'name': 'second-view',
                    'resources': ['my-resource'],
                    'spec': {'group': 'date', 'series': ['my-column'],
                             'type': 'bar'},
                    'specType': 'simple',
                    'title': 'My Second View Title'
                }
            ]
        }
        self.assertEqual(spew_dp, expected_dp)

    def test_add_datapackage_views_processor_dict(self):

        # input arguments used by our mock `ingest`
        datapackage = {
            'name': 'my-datapackage',
            'resources': []
        }
        params = {
            'views': ['tests/sample_data/sample-view-spec-dict.json']
        }

        # Path to the processor we want to test
        processor_dir = \
            os.path.dirname(datapackage_pipelines_ukds.processors.__file__)
        processor_path = os.path.join(processor_dir,
                                      'add_datapackage_views.py')

        # Trigger the processor with our mock `ingest` and capture what it will
        # returned to `spew`.
        spew_args, _ = mock_processor_test(processor_path,
                                           (params, datapackage, []))

        spew_dp = spew_args[0]

        # Asserts for the datapackage
        expected_dp = {
            'name': 'my-datapackage',
            'resources': [],
            'views': [
                {
                    'name': 'simple-view-bar',
                    'resources': ['my-resource'],
                    'spec': {'group': 'date', 'series': ['my-column'],
                             'type': 'bar'},
                    'specType': 'simple',
                    'title': 'My View Title'
                }
            ]
        }
        self.assertEqual(spew_dp, expected_dp)
