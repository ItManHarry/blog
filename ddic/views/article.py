'''
    文章信息维护
'''
from flask import Blueprint,url_for,render_template,redirect,flash,request
import uuid
from ddic.exts import db
from ddic.models import TbArticle,TbAuthor
from ddic.forms.all import ArticleForm
bp_article = Blueprint('article', __name__)
@bp_article.route('/index')
def index():
    #获取该作者所有的文章
    author_id = request.args.get('authorid')
    author = TbAuthor.query.get(author_id)
    articles = author.articles
    return render_template('article/index.html',articles=articles,author=author)
@bp_article.route('/add', methods=['GET','POST'])
def add():
    form = ArticleForm()
    author_id = request.args.get('authorid')
    author = TbAuthor.query.get(author_id)
    form.author_id.data = author_id
    if form.validate_on_submit():
        article = TbArticle(id=uuid.uuid4().hex,title=form.title.data,body=form.body.data,author_id=form.author_id.data)
        db.session.add(article)
        db.session.commit()
        flash('文章发布成功!')
        return redirect(url_for('.add',authorid=form.author_id.data))
    return render_template('article/add.html', form=form,author=author)