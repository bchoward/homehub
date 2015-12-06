#from homehub import homehub
from homehub.config import BaseConfiguration as conf
#from homehub import login_manager, mail
from paste.deploy.converters import aslist
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base





def setup_connection():
    # set up the engine for analytics db
    from meta import session
    from homehub.base import Base
    engine = create_engine(conf.DB_URI)
    session.configure(bind=engine)
    Base.metadata.bind = engine


def app_factory(global_config, **local_config):
    setup_connection()

    # mail for sending account notifications
    #mail.init_app(app)

    #register the users module blueprint
    #from analyticstool.app.users.views import mod as usersModule
    #app.register_blueprint(usersModule)

    #add our view as the login view to finish configuring the LoginManager
    #login_manager.login_view = "users.login_view"


    #----------------------------------------
    # logging
    #----------------------------------------

    import logging


    class ContextualFilter(logging.Filter):
        def filter(self, log_record):
            from flask import request
            from flask.ext.login import current_user
            log_record.url = request.path
            log_record.method = request.method
            log_record.ip = request.environ.get("REMOTE_ADDR")
            log_record.user_id = -1 if current_user.is_anonymous() else current_user.get_id()

            return True

    context_provider = ContextualFilter()
    homehub.logger.addFilter(context_provider)

    handler = logging.StreamHandler()

    log_format = "%(asctime)s\t%(levelname)s\t%(user_id)s\t%(ip)s\t%(method)s\t%(url)s\t%(message)s"
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)

    homehub.logger.addHandler(handler)

    from logging import ERROR
    from logging.handlers import TimedRotatingFileHandler

    # Only set up a file handler if we know where to put the logs
    if homehub.config.get("ERROR_LOG_PATH"):

        # Create one file for each day. Delete logs over 7 days old.
        file_handler = TimedRotatingFileHandler(homehub.config["ERROR_LOG_PATH"], when="D", backupCount=7)

        # Use a multi-line format for this logger, for easier scanning
        file_formatter = logging.Formatter('''
        Time: %(asctime)s
        Level: %(levelname)s
        Method: %(method)s
        Path: %(url)s
        IP: %(ip)s
        User ID: %(user_id)s

        Message: %(message)s

        ---------------------''')

        # Filter out all log messages that are lower than Error.
        file_handler.setLevel(ERROR)

        file_handler.setFormatter(file_formatter)
        homehub.logger.addHandler(file_handler)

    return homehub.wsgi_app


