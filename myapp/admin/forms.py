# external

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField


# internal

from ..models import Department, Role, Grade


class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RoleForm(FlaskForm):
    """
    Form for admin to add or edit role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class GradeForm(FlaskForm):
    paygrade = StringField('Pay Grade', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(), get_label="name")
    grade = QuerySelectField(query_factory=lambda: Grade.query.all(), get_label="paygrade")
    submit = SubmitField('Submit')


class AssignForm(FlaskForm):
    department = SelectField('Department', choices=[], validators=[DataRequired()])
    role = SelectField('Role', choices=[], validators=[DataRequired()])
    grade = SelectField('Grade', choices=[], validators=[DataRequired()])
    manager = SelectField('Manager', coerce=int, validators=[DataRequired()])


class AssignManagerForm(FlaskForm):
    manager = SelectField('Manager', coerce=int, validators=[DataRequired()])
    employee = SelectField('Employee', coerce=int, validators=[(DataRequired())])
    department = SelectField('Department', coerce=int)
    role = SelectField('Role', choices=[], validators=[DataRequired()])
    submit = SubmitField('Assign')