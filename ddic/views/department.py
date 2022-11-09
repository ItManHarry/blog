from flask import Blueprint,render_template,flash,url_for,redirect,request
from ddic.forms.all import DepartmentForm
from ddic.exts import db
from ddic.models import BizDepartment
from flask_login import login_required
import uuid
bp_department = Blueprint('department', __name__)
@bp_department.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    departments = BizDepartment.query.order_by(BizDepartment.code).all()
    return render_template('department/index.html', departments=departments)
@bp_department.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = DepartmentForm()
    form.parents.choices = [(department.id, department.name) for department in BizDepartment.query.order_by(BizDepartment.code).all()]
    if form.validate_on_submit():
        name = form.name.data
        root = form.root.data
        parent_id = form.parents.data
        if parent_id is None:
            root = True
        if root:
            code = generate_code('', len(BizDepartment.query.filter(BizDepartment.root == True).all()))
        else:
            parent = BizDepartment.query.get(parent_id)
            code = generate_code(parent.code, len(BizDepartment.query.filter(BizDepartment.parent_id == parent_id).all()))
        print('Department name is {}, is root {}, parent id {}.'.format(name, root, parent_id))
        department = BizDepartment(
            id=uuid.uuid4().hex,
            code=code,
            name=name,
            root=root,
            parent_id=parent_id if parent_id and not root else ''
        )
        db.session.add(department)
        db.session.commit()
        flash('部门信息添加成功!')
        return redirect(url_for('.index'))
    return render_template('department/edit.html', form=form)
@bp_department.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    department = BizDepartment.query.get(id)
    form = DepartmentForm()
    # 剔除自身及子部门
    form.parents.choices = [(department.id, department.name) for department in BizDepartment.query.filter(BizDepartment.id != id, BizDepartment.parent_id != id).order_by(BizDepartment.code).all()]
    if request.method == 'GET':
        form.name.data = department.name
        form.root.data = department.root
        form.parents.data = department.parent_id
    if form.validate_on_submit():
        department.name = form.name.data
        department.root = form.root.data
        if form.root.data:
            department.parent_id = ''
        else:
            department.parent_id = form.parents.data
        db.session.commit()
        flash('部门信息编辑成功!')
        return redirect(url_for('.index'))
    return render_template('department/edit.html', form=form)
def generate_code(parent_cd, parent_size):
    if parent_size < 10:
        return parent_cd+'0'+str(parent_size)
    else:
        return parent_cd+str(parent_size)