# external
from flask import render_template, abort, request, redirect, url_for, flash
from flask_login import login_required, current_user

# internal
from . import home
from .. import db
from ..admin.forms import AssignManagerForm
from ..models import Employee, Department, Role

# Constants
WORK_FROM_HOME_LIMIT = 10
LEAVE_DAYS_LIMIT = 21


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title='Welcome!')


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """

    return render_template('home/dashboard.html', title='Dashboard')


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    # Fetch all employees
    employees = Employee.query.all()

    # Fetch managers who are assigned as managers
    managers = Employee.query.filter_by(is_manager=True).all()

    return render_template('home/admin_dashboard.html', title='Dashboard', employees=employees, managers=managers)


@home.route('/admin/set_managers', methods=['GET', 'POST'])
@login_required
def set_managers():
    if not current_user.is_admin:
        abort(403)

    if request.method == 'POST':
        emp_id = request.form.get(('employee_id'))
        emp = Employee.query.get(emp_id)
        emp.is_manager = not emp.is_manager
        db.session.commit()
        return redirect(url_for('home.set_managers'))

    employees = Employee.query.all()

    return render_template('home/set_managers.html', employees=employees)


@home.route('/admin/appoint_manager', methods=['GET', 'POST'])
@login_required
def appoint_manager():
    if not current_user.is_admin:
        abort(403)

    form = AssignManagerForm()

    # Fetch all employees (to be assigned a manager)
    form.employee.choices = [(employee.id, employee.username) for employee in Employee.query.all()]

    # Fetch all departments
    form.department.choices = [(dept.id, dept.name) for dept in Department.query.all()]

    # Fetch all roles
    form.role.choices = [(role.id, role.name) for role in Role.query.all()]

    # Fetch the managers
    form.manager.choices = [(manager.id, manager.username) for manager in Employee.query.filter_by(is_manager=True).all()]

    if form.validate_on_submit():
        employee_id = form.employee.data
        employee = Employee.query.get(employee_id)
        manager_id = form.manager.data

        if employee:
            # Link the employee to the manager
            employee.manager_id = manager_id
            db.session.commit()
            flash(f'{employee.username} has been assigned to the manager {Employee.query.get(manager_id).username}!',
                  'success')

        department_id = form.department.data
        department = Department.query.get(department_id)
        if department:
            department.manager_id = manager_id
            db.session.commit()
            flash(f'Manager has been appointed to the department!', 'success')

        return redirect(url_for('home.appoint_manager'))

    return render_template('home/appoint_manager.html', form=form)


@home.route('/admin/employees')
@login_required
def admin_employees():
    if not current_user.is_admin:
        abort(403)

    return render_template('home/employees.html', title='Employees')


@home.route('/admin/view_employees', methods=['GET'])
@login_required
def view_managed_employees():
    if not current_user.is_manager:
        flash('You are not a manager!', 'error')
        return redirect(url_for('home.dashboard'))

    employees_managed = current_user.employees_managed
    return render_template('home/managed_employees.html', employees=employees_managed)


@home.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    return render_template('home/profilepage.html', title='Employee Profile')
