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

        oai_url = source['oai-url']

        for k, config in source['entries'].items():

            format = config['format']

            discovered_steps = cls._get_pipeline_steps()
            pipeline_id = slugify(k)

            if format in discovered_steps.keys():

                common_steps = [
                    ('add_metadata', {
                        'name': pipeline_id,
                        'oai_url': oai_url
                    })
                ]

                _steps = discovered_steps[format](common_steps,
                                                  pipeline_id, config)
                _steps = steps(*_steps)
            else:
                log.warn('No {} processor available for {}'.format(
                    format, pipeline_id))
                continue

            pipeline_details = {
                'pipeline': _steps
            }
            if schedule is not None:
                pipeline_details['schedule'] = {
                    'crontab': schedule
                }

            yield pipeline_id, pipeline_details
