# config.py

class Config(object):
    '''
    Common configurations
    '''

    # Put any configurations here that are common across all environments
    DEBUG = True

class DevelopmentConfig(object):
    '''
    Development configurations
    '''

    DEBUG = True
    # setting this to True activates the debug mode on the app.
    # This allows us to use the Flask debugger in case of an unhandled exception, and
    # also automatically reloads the application when it is updated.

    SQLALCHEMY_ECHO = True
    # setting this to True helps us with debugging by allowing SQLAlchemy to
    # log errors.


class ProductionConfig(object):
    '''
    Production configurations
    '''

    DEBUG = False


class TestingConfig(Config):
    '''
    Testing configurationa
    '''

    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}