import os

DOWNLOADS_PATH = os.path.join(os.path.dirname(__file__), '../../output')

label = 'spss'


def add_steps(steps: list, pipeline_id: str, config: dict) -> list:
    steps.append(('spss.add_spss', {
        'source': config['source']
    }))

    steps.append(('goodtables.validate', {
        'fail_on_error': True,
        'fail_on_warn': False
    }))

    steps.append(('dump.to_path', {
        'out-path': '{}/{}'.format(DOWNLOADS_PATH, pipeline_id)
    }))

    return steps
