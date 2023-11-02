from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username:", 
                           validators=[DataRequired("Це поле обовʼязкове")],
                           render_kw={"class": "form-control"})
    
    password = PasswordField("Password:", 
                             validators=[DataRequired("Це поле обовʼязкове"), 
                                         Length(min=4, max=10)],
                                         render_kw={"class": "form-control"})
    
    remember = BooleanField("Remember me", 
                            render_kw={"class": "form-check-input"})

    submit = SubmitField("Sign In", 
                         render_kw={"class": "btn btn-primary"})

    
class ChangePassword(FlaskForm):
    current_password = PasswordField("Current password:", 
                             validators=[DataRequired("Це поле обовʼязкове"), 
                                         Length(min=4, max=10)],
                                         render_kw={"class": "form-control"})
    new_password = PasswordField("New password:", 
                             validators=[DataRequired("Це поле обовʼязкове"), 
                                         Length(min=4, max=10)],
                                         render_kw={"class": "form-control"})
    submit_password = SubmitField("Change Password", 
                         render_kw={"class": "btn btn-primary"})
    

class FeedbackForm(FlaskForm):
    name = StringField("Username:", 
                           validators=[DataRequired("Це поле обовʼязкове")],
                           render_kw={"class": "form-control"})
    content = TextAreaField("Responde:", 
                           validators=[DataRequired("Це поле обовʼязкове")],
                           render_kw={"class": "form-control"})
    submit_feedback = SubmitField("Confirm", 
                         render_kw={"class": "btn btn-primary"})