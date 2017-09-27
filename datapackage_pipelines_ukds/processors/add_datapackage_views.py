import json
from datapackage_pipelines.wrapper import ingest, spew

import logging
log = logging.getLogger(__name__)

params, datapackage, resource_iterator = ingest()

dp_views = datapackage.get('views', [])
param_views = params['views']

for view_path in param_views:
    with open(view_path) as json_file:
        view_json = json.load(json_file)
        for v in view_json:
            dp_views.append(v)

datapackage['views'] = dp_views

spew(datapackage, resource_iterator)
