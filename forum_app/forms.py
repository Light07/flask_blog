#coding=utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, validators, TextAreaField, IntegerField
from wtforms.validators import Regexp
from wtforms.widgets import TextArea


# class CKEditorWidget(TextArea):
#     def __call__(self, field, **kwargs):
#         if kwargs.get('class'):
#             kwargs['class'] += " ckeditor"
#         else:
#             kwargs.setdefault('class', 'ckeditor')
#         return super(CKEditorWidget, self).__call__(field, **kwargs)
#
# class CKEditorField(TextAreaField):
#     widgets = CKEditorWidget()

class LoginForm(FlaskForm):
    username = StringField('User Name', [validators.DataRequired("Please enter your name")])
    password = PasswordField('Password', [validators.DataRequired("Please enter your password")])
    remember_me = BooleanField('remember_me', default=False)
    # login = SubmitField('登录'.decode('utf-8'))
    login = SubmitField('登录')

class SignUpForm(FlaskForm):
    username = StringField('UserName', [validators.DataRequired("Please enter your name")])
    phonenumber = StringField('phonenumber', [validators.Regexp('\d{11}', 0, 'Please enter valid phone number')])
    password = PasswordField('PassWord', [validators.DataRequired("Please enter your password")])
    pd_confirm = PasswordField('Confirm Password', [validators.DataRequired("Please reenter your password")])
    # signup = SubmitField('注册'.decode('utf-8'))
    signup = SubmitField('注册')

class AddcategoryForm(FlaskForm):
   name = StringField('NewCategory', validators=[validators.DataRequired("Please enter your name"), validators.Length(1, 64)])
   submit = SubmitField('Add')


class PostEditor(FlaskForm):
    # title = StringField('标题'.decode('utf-8'), [validators.DataRequired("Please enter your title")])
    # category = StringField('类别'.decode('utf-8'))
    # # post = CKEditorField('正文'.decode('utf-8'), validators=[validators.DataRequired()])
    # publish = SubmitField('发布'.decode('utf-8'))

    title = StringField('标题', [validators.DataRequired("Please enter your title")])
    category = StringField('类别')
    publish = SubmitField('发布')
