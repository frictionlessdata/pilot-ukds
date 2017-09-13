import os
import urllib

from datapackage_pipelines.generators import slugify

DOWNLOADS_PATH = os.path.join(os.path.dirname(__file__), '../../output')

label = 'csv'


def add_steps(steps: list, pipeline_id: str, config: dict) -> list:
    name = slugify(urllib.parse.unquote(os.path.basename(config['source'])))
    name = name.lower()
    add_resource_options = {
        'url': config['source'],
        'format': 'csv',
        'name': name
    }
    # Add tabulator options
    if 'tabulator' in config:
        add_resource_options.update(config['tabulator'])

    steps.append(('add_resource', add_resource_options))

    steps.append(('stream_remote_resources', {
        'resources': name
    }))

    steps.append(('goodtables.validate', {
        'fail_on_error': True,
        'fail_on_warn': False
    }))

    steps.append(('dump.to_path', {
        'out-path': '{}/{}'.format(DOWNLOADS_PATH, pipeline_id)
    }))

    return steps
