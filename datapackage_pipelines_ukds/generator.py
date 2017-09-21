import os
import json
import pkgutil

from datapackage_pipelines.generators import (
    GeneratorBase,
    steps,
    slugify,
    SCHEDULE_DAILY
)

from . import pipeline_steps

import logging
log = logging.getLogger(__name__)

DOWNLOADS_PATH = os.path.join(os.path.dirname(__file__), '../output')
SCHEMA_FILE = os.path.join(
    os.path.dirname(__file__), 'schemas/ukds_spec_schema.json')


class Generator(GeneratorBase):

    @staticmethod
    def _get_pipeline_steps() -> dict:
        '''
        Discover available pipeline steps under the `pipeline_steps` package.

        Returns a dict of their {label: add_steps} k/v pairs.
        '''
        pkgpath = os.path.dirname(pipeline_steps.__file__)

        pipeline_modules = [getattr(pipeline_steps, name) for _, name, _
                            in pkgutil.iter_modules([pkgpath])]

        available_steps = {}
        for module in pipeline_modules:
            if module.label and module.add_steps:
                available_steps.update({module.label: module.add_steps})

        return available_steps

    @classmethod
    def get_schema(cls):
        return json.load(open(SCHEMA_FILE))

    @classmethod
    def generate_pipeline(cls, source):
        schedule = SCHEDULE_DAILY

        discovered_steps = cls._get_pipeline_steps()

        for k, config in source['entries'].items():

            pipeline_id = slugify(k)

            _steps = [
                ('add_metadata', {
                    'name': pipeline_id
                })
            ]

            has_resources = False

            for resource in config['source']:
                format = resource['format']
                if format in discovered_steps.keys():
                    _steps = discovered_steps[format](_steps,
                                                      pipeline_id, resource)
                    has_resources = True
                else:
                    log.warn('No {} processor available for {}'.format(
                        format, pipeline_id))

            if not has_resources:
                continue

            _post_steps = []

            if 'oai-id' in config:
                _post_steps.append(('ukds.add_oai_metadata', {
                    'oai_id': config['oai-id'],
                    'oai_url': source['oai-url']
                }))

            _post_steps.append(('goodtables.validate', {
                'fail_on_error': True,
                'reports_path':
                    '{}/{}/{}'.format('../output', pipeline_id, 'reports'),
                'datapackage_reports_path': 'reports'
            }))

            _post_steps.append(('dump.to_path', {
                'out-path': '{}/{}'.format(DOWNLOADS_PATH, pipeline_id)
            }))

            _steps = _steps + _post_steps
            _steps = steps(*_steps)

            pipeline_details = {
                'pipeline': _steps
            }
            if schedule is not None:
                pipeline_details['schedule'] = {
                    'crontab': schedule
                }

            yield pipeline_id, pipeline_details
