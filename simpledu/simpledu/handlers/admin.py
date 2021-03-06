from flask import Blueprint, render_template, redirect, current_app, request, flash, url_for
from ..decorators import admin_required
from ..models import Course, db, User, Live
from ..forms import CourseForm, UserForm, LiveForm
admin = Blueprint('admin', __name__, url_prefix='/admin')
@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@admin.route('/courses')
@admin_required
def courses():
    page = request.args.get('page', default=1, type=int)
    pagination = Course.query.paginate(
        page = page,
        per_page = current_app.config['ADMIN_PER_PAGE'],
        error_out = False
    )

    return render_template('admin/courses.html', pagination=pagination)

@admin.route('/courses/create', methods=['GET', 'POST'])
@admin_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        form.create_course()
        flash('课程创建成功')
        return redirect(url_for('admin.courses'))
    return render_template('admin/create_course.html', form=form)

@admin.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        form.update_course(course)
        flash('课程更新成功', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/edit_course.html', form=form, course=course)

@admin.route('/courses/<int:course_id>/delete')
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('课程删除成功', 'success')
    return redirect(url_for('admin.courses'))

@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
        page = page,
        per_page= current_app.config['USER_PER_PAGE'],
        error_out = False
    )

    return render_template('admin/users.html', pagination = pagination)

@admin.route('/users/create_user', methods=['POST', 'GET'])
@admin_required
def create_user():
    form = UserForm()

    if form.validate_on_submit():
        form.create_user()
        flash('创建用户成功')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_user.html', form=form)

@admin.route('/users/<int:user_id>/edit', methods=['POST', 'GET'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.update_user(user)
        flash('用户资料修改成功', 'success')
        return redirect(url_for('.users'))
    return render_template('admin/edit_user.html', form = form, user = user)

@admin.route('/users/<int:user_id>/delete')
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('删除用户成功', 'success')
    return redirect(url_for('.users'))

@admin.route('/live')
@admin_required
def live():
    page = request.args.get('page', default=1, type=int)
    pagination = Live.query.paginate(
        page = page,
        per_page = current_app.config['LIVE_PER_PAGE'],
        error_out = False
    )
    return render_template('admin/live.html', pagination = pagination)

@admin.route('/live/create_live', methods=['POST', 'GET'])
@admin_required
def create_live():

    form = LiveForm()
    if form.validate_on_submit():
        form.create_live()
        flash('直播创建成功')
        return redirect(url_for('.live'))
    return render_template('admin/create_live.html', form = form )

@admin.route('/live/<int:live_id>/edit_live', methods=['POST', 'GET'])
@admin_required
def edit_live(live_id):
    live = Live.query.get_or_404(live_id)
    form = LiveForm(obj=live)
    if form.validate_on_submit():
        form.update_live(live)
        flash('直播资料已更新')
        return redirect(url_for('.live'))
    return render_template('admin/edit_live.html', form = form, live=live)

@admin.route('/live/<int:live_id>/delete_live', methods=['POST', 'GET'])
@admin_required
def delete_live(live_id):
    live = Live.query.get(live_id)
    db.session.delete(live)
    db.session.commit()
    return redirect(url_for('.live'))
