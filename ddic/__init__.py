from flask import Flask,render_template
from ddic.exts import bootstrap,moment,mail,ckeditor,db,migrate
from ddic.settings import config
from ddic.views.board import bp_board
from ddic.views.author import bp_author
from ddic.views.article import bp_article
from ddic.models import Admin,Category
import click
#创建Flask实例
def create_app(config_name=None):
    if config_name == None:
        config_name = 'dev_config'
    print('Configuration name is %s' %config_name)
    app = Flask('ddic')
    # 加载配置
    app.config.from_object(config[config_name])
    # 初始化Web全局跳转
    register_web_global_routes(app)
    # 配置错误页面跳转
    register_web_errors(app)
    # 注册全局函数/变量
    register_template_globals(app)
    # 注册扩展组件
    register_extensions(app)
    # 注册shell环境
    register_shell_context(app)
    # 注册自定义命令
    register_web_command(app)
    # 注册系统各个模块
    register_web_views(app)
    return app
#初始化Web全局跳转
def register_web_global_routes(app):
    @app.route('/start')
    def start():
        return '<h1>Hello !</h1>'
    @app.route('/')
    def index():
        return render_template('index.html')
    @app.route('/login')
    def login():
        from ddic.forms.all import LoginForm
        form = LoginForm()
        return render_template('login/login.html', form=form)
#配置错误页面跳转
def register_web_errors(app):
    @app.errorhandler(400)
    def request_invalid(e):
        return render_template('errors/400.html'), 400
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    @app.errorhandler(500)
    def inner_error(e):
        return render_template('errors/500.html'), 500
#注册全局函数&变量
def register_template_globals(app):
    from ddic.utils import get_time
    app.jinja_env.globals['get_time'] = get_time
    app.jinja_env.globals['admin_name'] = 'Harry.Cheng'
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin, categories=categories)
#注册扩展组件
def register_extensions(app):
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
#注册shell环境
def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)
#注册系统各个模块
def register_web_views(app):
    app.register_blueprint(bp_board, url_prefix='/board')
    app.register_blueprint(bp_author, url_prefix='/author')
    app.register_blueprint(bp_article, url_prefix='/article')

#注册自定义命令
def register_web_command(app):
    @app.cli.command()
    def initdb():
        db.create_all()
        click.echo('数据库初始化完成！！！')