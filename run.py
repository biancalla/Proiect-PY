import os

# internal
from myapp import create_app

'''
Creating the app by running the create_app function and
passing in the configuration name from the OS environment variable FLASK_CONFIG.
'''

config_name = os.getenv('FLASK_CONFIG')
if config_name is None:
    raise ValueError("Environment variable FLASK_CONFIG is not set.")
app = create_app()

if __name__ == '__main__':
    app.run()
