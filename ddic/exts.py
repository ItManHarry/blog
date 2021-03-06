'''
    Flask扩展
'''
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
#创建扩展实例
bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
mail = Mail()
ckeditor = CKEditor()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
'''
    配置login_required对应的跳转信息
'''
login_manager.login_view='auth.login'
login_manager.login_message='登录后才能进行相关操作!!!'
login_manager.login_message_category='warning'
'''
    加载用户
    注：集成flask-login后必须实现此方法，否则系统异常
'''
@login_manager.user_loader
def load_user(user_id):
    from ddic.models import Admin
    user = Admin.query.get(user_id)
    return user