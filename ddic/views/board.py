'''
    留言板模块
'''
from flask import Blueprint,render_template
from ddic.forms.board import MessageForm
bp_board = Blueprint('board', __name__)
@bp_board.route('/index', methods = ['GET','POST'])
def index():
    form = MessageForm()
    if form.validate_on_submit():
        pass
    return render_template('board/index.html', form=form)