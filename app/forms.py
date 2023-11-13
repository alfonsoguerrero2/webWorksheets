from flask_wtf import FlaskForm
from wtforms import IntegerField,  StringField
from wtforms.validators import DataRequired
from app.models import *


class CalculatorForm(FlaskForm):
    number1 = IntegerField('number1', validators=[DataRequired()])
    number2 = IntegerField('number2', validators=[DataRequired()])


class form_input(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    new_amount = IntegerField('new_income', validators=[DataRequired()])


class saving_goal(FlaskForm):
    goal_input = StringField('goal_input', validators=[DataRequired()])
