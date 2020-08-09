import os

development = {
    'project': {
        'project': 'junback',
        'version': '0.0.1',
        'mode': 'development',
        'description': 'Made with love <3 by Anton and sketches from MoonSolutions'
    },
    'db': {
        'host': 'db',
        'db': 'junback',
        'user': 'user',
        'password': 'password',
        'port': '5432'
    },
    'secure': {
        'salt_password': 'salt',
        'salt_session': 'session'
    }
}

app_mode = os.environ.get('APP_MODE', 'develop')
config = development
