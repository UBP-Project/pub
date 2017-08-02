import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    swagger_template = {
      "swagger": "2.0",
      "info": {
        "title": "UBP: PUB",
        "description": "API for UnionBank's PUB",
        "contact": {
          "responsibleOrganization": "UBP: Pub"
        },
        "version": "1.0.0"
      },
      "host": "localhost:5000",  # overrides localhost:500
      "basePath": "/",  # base bash for blueprint registration
      "schemes": [
        "http",
        "https"
      ],
      "operationId": "getmyData"
    }

    swagger_config = {
        "headers": [
        ],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        # "static_folder": "static",  # must be set by user
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://root:@localhost/pub_dev'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'mysql+pymysql://root:@localhost/pub_test'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:@localhost/pub_prod'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
