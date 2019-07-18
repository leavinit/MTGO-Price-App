from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField # PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class CardForm(FlaskForm):
    card_name = StringField('Card Name', validators=[DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # remember_me = BooleanField('Remember Me')
    submit = SubmitField('Get Prices')
