import os
import urllib

from datapackage_pipelines.wrapper import ingest, spew
from tabulator.helpers import detect_scheme_and_format

from datapackage_pipelines_ukds.oai_utils import OAI_Repository

import logging
log = logging.getLogger(__name__)


params, datapackage, res_iter = ingest()

oai_url = params['oai_url']
oai_id = params['oai_id']

oai_repo = OAI_Repository(oai_url)
record = oai_repo.get_oai_record_metadata(oai_id)


def _make_title_from_identifier(identifier):
    '''
    Attempts to extract the base filename from `identifier` if it is an http or
    filepath.
    '''
    source_scheme, _ = detect_scheme_and_format(identifier)
    if source_scheme in ['http', 'https', 'file']:
        title = urllib.parse.unquote(os.path.basename(identifier))
        if title == '':
            title = identifier
    else:
        title = identifier
    return title


if 'title' in record:
    datapackage['title'] = record['title'][0]

if 'description' in record:
    datapackage['description'] = record['description'][0]

if 'creator' in record:
    datapackage['contributors'] = \
        [{'title': c, 'role': 'author'} for c in record['creator']]

if 'relation' in record:
    datapackage['homepage'] = record['relation'][0]

if 'subject' in record:
    datapackage['keywords'] = [kw for kw in record['subject']]

if 'publisher' in record:
    datapackage['publisher'] = record['publisher'][0]

if 'identifier' in record:
    '''Discover sources from the OAI record. UKDS creates a erroneous last
    record, which is excluded here by looking for the string 'error in
    script'.'''
    datapackage['sources'] = \
        [{'title': _make_title_from_identifier(ider), 'path': ider}
         for ider in record['identifier'] if 'error in script' not in ider]


spew(datapackage, res_iter)
