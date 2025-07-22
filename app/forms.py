from wtforms.validators import DataRequired, Email, EqualTo, Length


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FloatField

# BetslipForm for dashboard betslip generator
class BetslipForm(FlaskForm):
    league = SelectField("League", choices=[], validators=[DataRequired()])
    market = SelectField("Market", choices=[], validators=[DataRequired()])
    min_odds = FloatField("Min Odds", validators=[DataRequired()])
    submit = SubmitField("Generate")

class AdminLoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login as Admin")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class SignupForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    role = StringField(
        "Role",
        default="user"
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=255)]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )
    confirm = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")]
    )
    submit = SubmitField("Sign Up")
    agree_terms = BooleanField(
        "I agree to the Terms and Conditions",
        validators=[DataRequired(message="You must agree to the terms.")]
    )
    privacy = BooleanField(
        "I accept the Privacy Policy",
        validators=[DataRequired(message="You must accept the privacy policy.")]
    )
