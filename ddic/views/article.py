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