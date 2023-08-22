# external
from flask import flash, redirect, render_template,url_for
from flask_login import login_required, current_user, login_user, logout_user

# internal
from . import auth
from .forms import LoginForm, RegistrationForm, ResetPasswordForm
from .. import db
from ..models import Employee


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle request to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        # add employee to the database
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully registered! You can log in.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle request to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether the password entered
        # matches the password in the database
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(form.password.data):
            # log employee in
            login_user(employee)

            # redirect to the appropriate dashboard page
            if employee.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    """
    Handle request to the /reset_password route
    Reset the password of an employee through the reset password
    """
    # check whether employee is logged in
    if current_user.is_authenticated:
        # redirect to the dashboard page
        return redirect(url_for('home.dashboard'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()

        # check whether the password entered matches the password in the database
        if employee:
            employee.password = form.password.data
            db.session.commit()
            flash('Your password has been updated!', 'success')

            # redirect to the login page
            return redirect(url_for('auth.login'))

        # when login details are incorrect
        else:
            flash('Email not found!', 'danger')

    # load reset password template
    return render_template('auth/reset_password.html', title='Reset password', form=form)


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have been successfully been logged out!')

    # redirect to the login page
    return redirect(url_for('auth.login'))
