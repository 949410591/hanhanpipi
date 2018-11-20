from flask_wtf import FlaskForm
from flask import request
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, IntegerField
from wtforms.validators import Length, Email, EqualTo, DataRequired, URL, NumberRange
from .models import User, db, Course, Live

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(3, 24)])
    email = StringField('email', validators = [DataRequired(), Email()])
    password = PasswordField('password', validators= [DataRequired(), Length(6,24)])
    repeat_password = PasswordField('repeat_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('submit')
    def validate_username(self, field):
    	if User.query.filter_by(username=field.data).first():
            raise ValidationError('username is exist')
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email is exist')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators= [DataRequired(), Length(6,24)])
    remember_me = BooleanField('remember_me')
    submit = SubmitField('submit')

    def validate_email(self, field):
        if not User.query.filter_by(email=self.email.data).first():
            raise ValidationError('email is error')
    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(self.password.data):
            raise ValidationError('password  is error')

class CourseForm(FlaskForm):
    name = StringField('课程名称', validators=[DataRequired(), Length(5, 32)])
    description = TextAreaField('课程简介', validators=[DataRequired(), Length(20, 256)])
    image_url = StringField('封面图片', validators=[DataRequired(), URL()])
    author_id = IntegerField('作者ID', validators=[DataRequired(), NumberRange(min=1, message='无效的用户ID')])
    submit = SubmitField('提交')

    def validate_author_id(self, field):
        if not User.query.get(self.author_id.data):
            raise ValidationError('用户不存在')

    def validate_name(self, field):
        if Course.query.filter_by(name = self.name.data).first():
            raise ValidationError('课程名已存在')

    def create_course(self):
        course =Course()
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self, course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

class UserForm(FlaskForm):
    id = IntegerField('ID', validators = [DataRequired(), NumberRange(min=1, message= '无效ID')])
    username = StringField('用户名', validators = [DataRequired(), Length(3, 24)])
    email = StringField('email', validators = [DataRequired(), Email()])
    password = PasswordField('密码', validators = [ DataRequired(), Length(6,24)])

    role = IntegerField('Role', validators = [ DataRequired()])
    job = StringField('工作', validators = [ DataRequired()])
    submit = SubmitField('提交')


    def validate_username(self, field):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('用户名已存在')

    def validate_id(self, field):

        if User.query.get(self.id.data):
            raise ValidationError('ID已存在')

    def validate_email(self, field):
        if User.query.filter_by(email = self.email.data).first() :
            raise ValidationError('邮箱已存在')


    def validate_role(self, field):
        role = self.role.data
        if not(role == 30 or role == 10 or role == 20):
            raise ValidationError('权限设置错误')

    def create_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user


    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

class LiveForm(FlaskForm):
    name = StringField('直播名', validators = [DataRequired(), Length(10,35)])
    user_id = IntegerField('用户id', validators = [DataRequired(),NumberRange(min=1, message='无效ID')])
    submit = SubmitField('submit')

    def validate_user_id(self, field):
        if Live.query.filter_by(user_id=field.data).first():
            raise ValidationError('该用户已有直播')

        if not User.query.get(field.data):
            raise ValidationError('没有该用户')


    def create_live(self):
        live = Live()
        self.populate_obj(live)
        db.session.add(live)
        db.session.commit()
        return live

    def update_live(self, live):
        self.populate_obj(live)
        db.session.add(live)
        db.session.commit()
        return live
