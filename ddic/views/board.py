'''
    留言板模块
'''
from flask import Blueprint,render_template,flash,url_for,redirect
from ddic.forms.board import MessageForm
from ddic.exts import db
from ddic.models import TbMessage
import uuid
bp_board = Blueprint('board', __name__)
@bp_board.route('/index', methods = ['GET','POST'])
def index():
    messages = TbMessage.query.order_by(TbMessage.timestamp.desc()).all()
    form = MessageForm()
    if form.validate_on_submit():
        message = TbMessage(id=uuid.uuid4().hex, title=form.title.data, body=form.body.data)
        db.session.add(message)
        db.session.commit()
        flash('消息已发布!!!')
        return redirect(
            url_for('.index'))  # 重定向index视图,获取最新数据,使用蓝本，url_for需要将endpoint添加完整"board.index"，本蓝本内加点即可".index"
    return render_template('board/index.html', form=form, messages=messages)