'''
    作者信息维护
'''
from flask import Blueprint, url_for,redirect,render_template,flash,request
from ddic.forms.all import AuthorForm
from ddic.exts import db
from ddic.models import TbAuthor
import uuid
bp_author = Blueprint('author', __name__)
'''
    作者信息主页(新增/列表/删除)
'''
@bp_author.route('/index', methods=['GET','POST'])
def index():
    authors = TbAuthor.query.order_by(TbAuthor.timestamp.desc()).all()
    form = AuthorForm()
    if form.validate_on_submit():
        print('save the author information!!!')
        author = TbAuthor(id=uuid.uuid4().hex,name=form.name.data,phone=form.phone.data)
        db.session.add(author)
        db.session.commit()
        flash('作者信息已保存！')
        return redirect(url_for('.index'))
    return render_template('author/index.html', form=form, authors=authors)
'''
    作者信息修改
'''
@bp_author.route('/edit', methods=['GET','POST'])
def edit():
    form = AuthorForm()
    if request.method == 'GET':
        id = request.args.get('id')
        author = TbAuthor.query.get(id)
        form.name.data = author.name
        form.phone.data = author.phone
        form.id.data = id
    if form.validate_on_submit():
        author = TbAuthor.query.get(form.id.data)
        author.name = form.name.data
        author.phone = form.phone.data
        db.session.commit()
        flash('修改成功！')
        return redirect(url_for('.edit', id=form.id.data))
    return render_template('author/edit.html', form=form,author=author)
@bp_author.route('/delete')
def delete():
    id = request.args.get('id')
    author = TbAuthor.query.get(id)
    db.session.delete(author)
    db.session.commit()
    return redirect(url_for('.index'))