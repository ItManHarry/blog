from flask import Flask,render_template
from ddic.exts import bootstrap,moment,mail,ckeditor,db
from ddic.settings import config
#创建Flask实例
def create_app(config_name=None):
    if config_name == None:
        config_name = 'dev_config'
    print('Configuration name is %s' %config_name)
    app = Flask('ddic')
    #加载配置
    app.config.from_object(config[config_name])
    #初始化Web全局跳转
    register_web_global_routes(app)
    #配置错误页面跳转
    register_web_errors(app)
    #注册全局函数/变量
    register_template_globals(app)
    #注册扩展组件
    register_extensions(app)
    return app
#初始化Web全局跳转
def register_web_global_routes(app):
    @app.route('/start')
    def start():
        return '<h1>Hello !</h1>'
    @app.route('/')
    def index():
        return render_template('index.html')
#配置错误页面跳转
def register_web_errors(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    @app.errorhandler(500)
    def inner_error(e):
        return render_template('errors/500.html'), 500
#注册全局函数
def register_template_globals(app):
    from ddic.utils import get_time
    app.jinja_env.globals['get_time'] = get_time
    app.jinja_env.globals['admin_name'] = 'Harry.Cheng'
#注册扩展组件
def register_extensions(app):
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    db.init_app(app)