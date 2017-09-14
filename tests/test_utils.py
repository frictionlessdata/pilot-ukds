import os
import unittest

import mock

from sickle import OAIResponse
from sickle._compat import to_unicode

from datapackage_pipelines_ukds.oai_utils import OAI_Repository

'''
MockResponse and mock_harvest taken from sickle's testing framework:
https://github.com/mloesch/sickle/blob/4def379aabe6af812a2cc12e843a3583d0fffcba/sickle/tests/test_harvesting.py
[BSD]
'''


this_dir, this_filename = os.path.split(__file__)


class MockResponse(object):
    """Mimics the response object returned by HTTP requests."""

    def __init__(self, text):
        # request's response object carry an attribute 'text' which contains
        # the server's response data encoded as unicode.
        self.text = text


def mock_harvest(*args, **kwargs):
    """Read test data from files instead of from an OAI interface.

    The data is read from the ``xml`` directory by using the provided
    :attr:`verb` as file name. The following returns an OAIResponse created
    from the file ``ListRecords.xml``::

        fake_harvest(verb='ListRecords', metadataPrefix='oai_dc')

    The file names for consecutive resumption responses are expected in the
    resumptionToken parameter::

        fake_harvest(verb='ListRecords', resumptionToken='ListRecords2.xml')

    The parameter :attr:`error` can be used to invoke a specific OAI error
    response. For instance, the following returns a ``badArgument`` error
    response::

        fake_harvest(verb='ListRecords', error='badArgument')

    :param kwargs: OAI arguments that would normally be passed to
                   :meth:`sickle.app.Sickle.harvest`.
    :rtype: :class:`sickle.response.OAIResponse`.
    """
    verb = kwargs.get('verb')
    resumption_token = kwargs.get('resumptionToken')
    error = kwargs.get('error')
    if resumption_token is not None:
        filename = resumption_token
    elif error is not None:
        filename = '%s.xml' % error
    else:
        filename = '%s.xml' % verb

    with open(os.path.join(this_dir, 'sample_data', filename), 'r') as fp:
        response = MockResponse(to_unicode(fp.read()))
        return OAIResponse(response, kwargs)


class TestBase(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super(TestBase, self).__init__(methodName)
        self.patch = mock.patch('sickle.app.Sickle.harvest', mock_harvest)

    def setUp(self):
        self.patch.start()
        self.oai_repo = OAI_Repository('http://localhost')

    def tearDown(self):
        self.patch.stop()
