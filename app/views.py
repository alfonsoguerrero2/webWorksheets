from flask import render_template, flash, request
from app import app
from .forms import CalculatorForm, form_input, saving_goal
from app.models import *
from app import db
from sqlalchemy.exc import IntegrityError
from flask import redirect


# all the functions for the home pag
@app.route('/', methods=['GET', 'POST'])
def home():
    # calculate the total money the user
    # by adding all the incomes - expenses
    incomes = Incomes.query.all()
    expenses = expenditures.query.all()
    total = 0
    for income in incomes:
        total = total + income.amount
    for expend in expenses:
        total = total - expend.amount

    # goals section of the home page
    goal_form = saving_goal()
    if goal_form.validate_on_submit():

        # it will check(exist) if there is a existing goal
        exist = goal_class.query.first()
        if exist:
            return render_template('Home.html', title='Home', total=total,
                                   goal_form=goal_form, goal=exist,
                                   show_goal_form=show_goal_form(),
                                   calculate_progress=calculate_progress())

        # if there is not an erxisting goal it will create one(goal_record)
        # with the goal_form input values
        else:
            goal_input = goal_form.goal_input.data
            goal_record(goal_input)
            flash('Successfully received form data. %s' % (goal_input))
    exist = goal_class.query.first()
    return render_template('Home.html', title='Home', total=total, goal=exist,
                           goal_form=goal_form,
                           show_goal_form=show_goal_form(),
                           calculate_progress=calculate_progress())


# check existing goal record
def show_goal_form():
    if goal_class.query.first():
            return False
    else:
            return True


# calculate the progress by comparing the total money
# with the goal
def calculate_progress():
    current_goal = goal_class.query.first()
    incomes = Incomes.query.all()
    expenses = expenditures.query.all()
    total = 0
    for income in incomes:
        total = total + income.amount

    for expend in expenses:
        total = total - expend.amount

    if current_goal:
        return (int(total) / current_goal.store_goal) * 100
    return 0


# access goal records and delete them
@app.route('/eliminate_goals', methods=['POST'])
def eliminate_goals():
    try:
        goal_class.query.delete()
        db.session.commit()
        flash("All goals have been eliminated.", "success")
    except Exception as e:
        flash("Error eliminating goals: {}".format(e), "error")

    # go back to the home page
    return redirect('/')


# take the goal amount input by the user on a form
# create a record with it
def goal_record(goal_value):
    try:
        # Create a new record in the Incomes table
        goal_record = goal_class(store_goal=goal_value)
        db.session.add(goal_record)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("A record with this name already exists.", "error")
    return redirect('/home')


# all the functions for the income #
@app.route('/income', methods=['GET', 'POST'])
def income_form():

    # take user input with form
    # make a record with the inputted values
    form = form_input()
    if form.validate_on_submit():
        name = form.name.data
        new_amount = form.new_amount.data
        income_record(new_amount, name)
    return render_template('incomes.html', form=form, title='income')


# take the inputted values and make income record
def income_record(new_income, name):
    try:
        # Create a new record in the Incomes table
        income_record = Incomes(name=name, amount=new_income)
        db.session.add(income_record)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("A record with this name already exists.", "error")
    return redirect('/income')


# shows all the income records
@app.route('/income_table', methods=['GET', 'POST'])
def income_table():
    incomes = Incomes.query.all()
    return render_template('incomes_table.html',
                           incomes=incomes, title='income_table')


# income id of the record is pass a parameter so it can be deleted
@app.route('/delete_income/<int:income_id>', methods=['GET', 'POST'])
def delete_income(income_id):
    income = Incomes.query.get(income_id)
    if income:
        db.session.delete(income)
        db.session.commit()
        flash("Income record {income_id} deleted successfully.", "success")
    else:
        flash("Income record {income_id} not found.", "error")
    return redirect('/income_table')  # Redirect back to the display page


# take the income id of a record
# ask for an input
# call edit_record1() with the record and inputted values
@app.route('/edit_income/<int:income_id>', methods=['GET', 'POST'])
def edit_income(income_id):
    income = Incomes.query.get(income_id)
    form = form_input()
    if form.validate_on_submit():
        name = form.name.data
        new_amount = form.new_amount.data
        edit_record1(new_amount, name, income)
        return redirect('/income_table')
    return render_template('edit.html', form=form,
                           income=income, title='edit_income')


# takes a income record, string, int input by the user
# takes the last 2 args and update the record with those values
def edit_record1(new_income, name, income):
    try:
        income.name = name
        income.amount = new_income
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("A record with this name already exists.", "error")
    return redirect('/income_table')


# functions for expenses #


@app.route('/expenses', methods=['GET', 'POST'])
def expenses_form():
    # take user input with form
    # make a record with the inputted values
    form = form_input()
    if form.validate_on_submit():
        name = form.name.data
        new_amount = form.new_amount.data
        expenses_record(new_amount, name)
    return render_template('expenses.html', form=form, title='expenses')


# take the inputted values and make expendatures record
def expenses_record(new_expenses, name):
    try:
        # Create a new record in the Incomes table
        expense_record = expenditures(name=name, amount=new_expenses)
        db.session.add(expense_record)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("A record with this name already exists.", "error")
    return redirect('/expenses')


# shows all the expenses records
@app.route('/expenses_table', methods=['GET', 'POST'])
def expenses_table():
    expenses = expenditures.query.all()
    return render_template('expenses_table.html',
                           expenses=expenses, title='expenses_table')


# income id of the record is pass a parameter si it can be deleted
@app.route('/delete_expend/<int:expend_id>', methods=['GET', 'POST'])
def delete_expend(expend_id):
    expend = expenditures.query.get(expend_id)
    if expend:
        db.session.delete(expend)
        db.session.commit()
        flash("Income record {expend_id} deleted successfully.", "success")
    else:
        flash("Income record {expend_id} not found.", "error")
    return redirect('/expenses_table')  # Redirect back to the display page


# take the expend id of a record
# ask for an input
# call edit_record2() with the record and inputted values
@app.route('/edit_expend/<int:expend_id>', methods=['GET', 'POST'])
def edit_expend(expend_id):
    expend = expenditures.query.get(expend_id)
    form = form_input()
    if form.validate_on_submit():
        name = form.name.data
        new_amount = form.new_amount.data
        edit_record2(new_amount, name, expend)
        return redirect('/expenses_table')
    return render_template('edit_ex.html', form=form,
                           expend=expend, title='edit_expend')


# takes a expend record, string, int input by the user
# takes the last 2 args and update the record with those values
def edit_record2(new_expend, name, expend):
    try:
        # Create a new record in the Incomes table
        expend.name = name
        expend.amount = new_expend
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("A record with this name already exists.", "error")
    return redirect('/expenses_table')
