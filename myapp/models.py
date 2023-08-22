# external

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# internal

from myapp import db, login_manager


class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    subordinates = db.relationship('Employee', back_populates='manager', remote_side=[id])
    manager = db.relationship('Employee', back_populates='subordinates', foreign_keys=[manager_id])
    is_admin = db.Column(db.Boolean, default=False)
    is_manager = db.Column(db.Boolean, default=False)

    @property
    def password(self):

        # Preventing password from being accessed
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):

        # Set password to a hashed password
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):

        # Check if hashed password matches actual password
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


"""
Set up user_loader, which Flask-login uses to reload the user object
from the user ID stored in the session
"""
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

class Department(db.Model):

    # Create a Department table
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department', lazy='dynamic', foreign_keys=[Employee.department_id])
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

    def __repr__(self):
        return '{}'.format(self.name)

class Role(db.Model):

    # Create a Role table
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)


class Grade(db.Model):

    # Create a Pay Grade table
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    paygrade = db.Column(db.String(60), unique=True)
    amount = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='grade',
                                lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.paygrade)
