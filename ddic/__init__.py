from flask import Flask,render_template,redirect,url_for,make_response
from flask_wtf.csrf import CSRFError
from flask_login import current_user
from ddic.exts import bootstrap,moment,mail,ckeditor,db,migrate,login_manager,csrf
from ddic.settings import config
from ddic.views.board import bp_board
from ddic.views.author import bp_author
from ddic.views.article import bp_article
from ddic.views.blog import bp_blog
from ddic.views.auth import bp_auth
from ddic.views.admin import bp_admin
from ddic.views.department import bp_department
from ddic.models import Admin,Category,Comment,Post
from ddic.utils import redirect_back
import click
import uuid
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
        return redirect(url_for('blog.index'))
    @app.route('/back')
    def go_back():
        response = make_response(redirect_back())
        return response
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
    @app.errorhandler(CSRFError)
    def csrf_error(e):
        return render_template('errors/csrf.html')
#注册全局函数&变量
def register_template_globals(app):
    from ddic.utils import get_time
    app.jinja_env.globals['get_time'] = get_time
    app.jinja_env.globals['admin_name'] = 'Harry.Cheng'
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()                                                 #管理员
        categories = Category.query.order_by(Category.name).all()                   #文章分类
        post_cout = Post.query.count()                                              #文章数量
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()       #未读评论
        else:
            unread_comments = None
        return dict(admin=admin, categories=categories,unread_comments=unread_comments,post_cout=post_cout)
#注册扩展组件
def register_extensions(app):
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
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
    app.register_blueprint(bp_blog, url_prefix='/blog')
    app.register_blueprint(bp_auth, url_prefix='/auth')
    app.register_blueprint(bp_admin, url_prefix='/admin')
    app.register_blueprint(bp_department, url_prefix='/department')
#注册自定义命令
def register_web_command(app):
    #初始化系统
    @app.cli.command()
    @click.option('--username', prompt=True, help='管理员账号.')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True,help='管理员密码.')
    def init(username, password):
        click.echo('执行数据库初始化......')
        db.create_all()
        click.echo('数据库初始化完成！！！')
        click.echo('创建管理员')
        admin = Admin.query.first()
        if admin:
            click.echo('管理员已存在,跳过创建......')
        else:
            click.echo('执行创建管理员......')
            admin = Admin(
                id = uuid.uuid4().hex,
                username=username,
                blog_title = 'BlueBlog',
                blog_sub_title = 'If you want to do something, JUST DO IT!!!',
                name = 'Administrator',
                about = 'This is a Python blog!'
            )
            admin.set_password(password)
            db.session.add(admin)
        click.echo('执行创建默认类别......')
        category = Category.query.first()
        if category is None:
            click.echo('创建默认类别......')
            category = Category(id=uuid.uuid4().hex,name='默认')
            db.session.add(category)
        else:
            click.echo('类别已有记录,跳过创建......')
        db.session.commit()
        click.echo('系统初始化完成......')