"""
Entry point for starting the application along with `app.py`.

They're meant to be more or less identical, but there may be some differences between the two.
"""
import pathlib

from apscheduler.schedulers.background import BackgroundScheduler
from flask_login import LoginManager
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

from pytheas import app
# noinspection PyUnresolvedReferences
import pytheas.views
import os
import cherrypy
from pytheas.config import config
from paste.translogger import TransLogger

import dotenv

from pytheas.data import mongo_setup

dotenv.load_dotenv('../.env')


def mkdir_p(path):
    os.makedirs(path, exist_ok=True)
    return path


def prepare_config(debug=False):
    app.config['LOG_DIR'] = mkdir_p(os.path.join(app.config['BASE_DIR'], 'logs'))
    app.debug = debug

    app.secret_key = app.config['SECRET_KEY']


def run_cherrypy_server(port=8090):
    app_logged = TransLogger(app, logger=app.logger, setup_console_handler=False)
    cherrypy.tree.graft(app_logged, '/')
    cherrypy.tree.mount(None, '/static', config={})
    cherrypy.config.update(
        {
            'engine.autoreload.on': False,
            'log.screen': True,
            'server.socket_port': port,
            'server.socket_host': '0.0.0.0',
        }
    )
    if hasattr(cherrypy.engine, 'signal_handler'):
        cherrypy.engine.signal_handler.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()


def setup_login():
    from pytheas.data.users import User
    login_manager = LoginManager()
    login_manager.login_view = 'login.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(pk=user_id).first()


def run_tornado_server(port=8090):
    """
    TODO: enable logging
    :param port:
    :return:
    """
    server = HTTPServer(WSGIContainer(app))
    server.listen(port)
    IOLoop.instance().start()


def register_blueprints():
    from pytheas.views import home_views
    from pytheas.views import review_views
    from pytheas.views import admin_views
    from pytheas.views import login_view
    from pytheas.views import project_views
    from pytheas.views import tool_views

    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(review_views.blueprint)
    app.register_blueprint(admin_views.blueprint)
    app.register_blueprint(login_view.blueprint)
    app.register_blueprint(project_views.blueprint)
    app.register_blueprint(tool_views.blueprint)


def create_scheduled_jobs():
    from pytheas.tasks.load_data import load_data

    app.config['DATA_DIR'] = mkdir_p(os.path.join(app.config['BASE_DIR'], 'data'))
    scheduler = BackgroundScheduler()
    scheduler.add_job(load_data, 'cron', hour='23', minute='30', timezone='America/Los_Angeles',
                      misfire_grace_time=120)
    scheduler.start()


def main():
    server = os.environ.get('SERVER', '')
    port = int(os.environ.get('FLASK_PORT', 8090))
    env = os.environ.get('FLASK_ENV', 'development')
    debug = env == 'development'
    app.config.from_object(config[env])
    app.config.from_mapping(**dict(os.environ))
    prepare_config(debug)
    mongo_setup.global_init()
    register_blueprints()
    create_scheduled_jobs()
    setup_login()
    if server == 'cherrypy':
        run_cherrypy_server(port=port)
    elif server == 'tornado':
        run_tornado_server(port=port)
    else:
        app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == '__main__':
    main()
