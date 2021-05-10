from flask import Blueprint, redirect,url_for,render_template,session,request,flash,current_app,abort,make_response
from flask_login import login_user,current_user,logout_user, login_required
from ddic.models import Admin,Login
from ddic.forms.all import LoginForm
from ddic.exts import db
from ddic.utils import redirect_back
import uuid
bp_auth = Blueprint('auth', __name__)
#登录
@bp_auth.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    form = LoginForm()
    next = request.args.get('next')
    print('Request path is >>>>>>>>>>>>>>>>>>>>>>>>>>>>>: ' , next)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.filter_by(username=username.lower()).first()
        if admin:
            if admin.validate_password(password):
                login_user(admin, remember)
                #新增登录履历
                login = Login(id=uuid.uuid4().hex,admin_id=admin.id)
                db.session.add(login)
                db.session.commit()
                return redirect_back()
            else:
                flash('密码错误!!!')
        else:
            flash('账号不存在!!!')
    return render_template('auth/login.html', form=form)
#登出
@bp_auth.route('/logout')
#@login_required
def logout():
    logout_user()
    return redirect(url_for('blog.index'))