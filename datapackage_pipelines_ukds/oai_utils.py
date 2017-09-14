from functools import lru_cache

from sickle import Sickle

import logging
log = logging.getLogger(__name__)

METADATA_PREFIX = 'oai_dc'


class OAI_Repository():

    def __init__(self, oai_url):
        self.repository = Sickle(oai_url)

    @lru_cache(maxsize=32)
    def _get_oai_identify_object(self):
        '''
        Get an oai Identify object for `oai_url`.
        '''
        return self.repository.Identify()

    def get_oai_record_identifier(self, record_id):
        '''
        Get an oai record identifier string for `record_id`.

        <scheme><delimiter><repositoryIdentifier><delimiter><record_id>
        '''

        identify_obj = self._get_oai_identify_object()
        return "{scheme}{delim}{repo_id}{delim}{record_id}".format(
            scheme=identify_obj.scheme,
            delim=identify_obj.delimiter,
            repo_id=identify_obj.repositoryIdentifier,
            record_id=record_id
        )

    def get_oai_record_metadata(self, record_id):

        record_identifier = self.get_oai_record_identifier(record_id)

        return self.repository.GetRecord(
            identifier=record_identifier,
            metadataPrefix=METADATA_PREFIX).metadata
