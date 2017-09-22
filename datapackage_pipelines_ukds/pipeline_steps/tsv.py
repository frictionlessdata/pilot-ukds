import os
import urllib

from datapackage_pipelines.generators import slugify

label = 'tsv'


def add_steps(steps: list, pipeline_id: str, config: dict) -> list:
    name = slugify(urllib.parse.unquote(os.path.basename(config['url'])))
    name = name.lower()
    add_resource_options = {
        'url': config['url'],
        'format': 'tsv',
        'name': name
    }
    # Add tabulator options
    if 'tabulator' in config:
        add_resource_options.update(config['tabulator'])

    steps.append(('add_resource', add_resource_options))

    steps.append(('stream_remote_resources', {
        'resources': name
    }))

    return steps
