from app import app
from flask import Flask, render_template, flash, redirect, url_for
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from app.forms import EditProfileForm
from app.forms import CreateMoveForm
from app.forms import EditMoveForm
from datetime import timedelta
from datetime import datetime
from app.timer import countdown_timer

################################ DONE THIS FUNCTION ##########################################
@app.before_request
def before_request():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first_or_404()
        # print('In before request')
        # print('User move date: {}'.format(user.move_date))
        # print('User future street address: {}'.format(user.future_street_address))
        # print('User future city: {}'.format(user.future_city))
        # print('User future state: {}'.format(user.future_state))
        # print('User future zip code: {}'.format(user.future_zip_code))
        if user.is_moving:
            # check their move date to see
            # if the timer expired
            if countdown_timer(user.move_date) <= timedelta(0,0,0):
                user.is_moving = False
                db.session.commit()
                user.move_date = None
                db.session.commit()

                user.current_street_address = user.future_street_address
                db.session.commit()
                user.current_city = user.future_city
                db.session.commit()
                user.current_state = user.future_state
                db.session.commit()
                user.current_zip_code = user.future_zip_code
                db.session.commit()

                user.future_street_address = None
                db.session.commit()
                user.future_city = None
                db.session.commit()
                user.future_state = None
                db.session.commit()
                user.future_zip_code = None
                db.session.commit()
################################ DONE THIS FUNCTION ##########################################

################################ DONE THIS FUNCTION ##########################################
@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title = 'Your Account - Water America')
################################ DONE THIS FUNCTION ##########################################

################################ DONE THIS FUNCTION ##########################################
@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        print('form was validated')
        user = User(
            last_name = form.last_name.data,
            first_name = form.first_name.data,
            current_street_address = form.street_address.data,
            current_city = form.city.data,
            current_state = form.state.data,
            current_zip_code = form.zip_code.data,
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered Water America customer!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
################################ DONE THIS FUNCTION ##########################################

################################ DONE THIS FUNCTION ##########################################
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
################################ DONE THIS FUNCTION ##########################################

################################ DONE THIS FUNCTION ##########################################
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
################################ DONE THIS FUNCTION ##########################################

################################ DONE THIS FUNCTION ##########################################
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
################################ DONE THIS FUNCTION ##########################################

################################ DONE THIS FUNCTION ##########################################
@app.route('/create_move', methods=['GET', 'POST'])
@login_required
def create_move():
    form = CreateMoveForm()
    user = User.query.filter_by(username=current_user.username).first_or_404()

    if user.is_moving:
        return redirect(url_for('edit_move'))

    if form.validate_on_submit():
        if user.current_city == form.city.data and user.current_state == form.state.data\
            and user.current_street_address == form.street_address.data\
                and user.current_zip_code == form.zip_code.data:
            flash('You must enter an address different from your current address.')
            redirect(url_for('create_move'))
        else:
            user.future_street_address = form.street_address.data
            db.session.commit()
            user.future_city = form.city.data
            db.session.commit()
            user.future_state = form.state.data
            db.session.commit()
            user.future_zip_code = form.zip_code.data
            db.session.commit()
            user.is_moving = True
            db.session.commit()
            user.move_date = datetime.strptime(form.move_date.data, '%m/%d/%Y')
            db.session.commit()
                            
            flash('Thank you for choosing Water America. Your move has been submitted.')
            return redirect(url_for('index'))
    
    elif request.method == 'GET':
        form.move_date.data = 'mm/dd/yyyy'
    
    return render_template('create_move.html', title='Create Move',form=form)
################################ DONE THIS FUNCTION ##########################################

################################ DONE THIS FUNCTION ##########################################
@app.route('/edit_move', methods=['POST', 'GET'])
@login_required
def edit_move():
    form = EditMoveForm()
    user = User.query.filter_by(username=current_user.username).first_or_404()
    if user.is_moving:
        if form.validate_on_submit():
            if form.delete.data:
                user.is_moving = False
                db.session.commit()
                user.move_date = None
                db.session.commit()
                user.future_street_address = None
                db.session.commit()
                user.future_city = None
                db.session.commit()
                user.future_state = None
                db.session.commit()
                user.future_zip_code = None
                db.session.commit()
                flash('Your move has been deleted.')
                return redirect(url_for('index'))
            if form.submit.data:
                user.move_date = datetime.strptime(form.move_date.data, '%m/%d/%Y')
                db.session.commit()
                user.future_street_address = form.street_address.data
                db.session.commit()
                user.future_city = form.city.data
                db.session.commit()
                user.future_state = form.state.data
                db.session.commit()
                user.future_zip_code = form.zip_code.data
                db.session.commit()
                flash('Your move has been updated.')
                return redirect(url_for('edit_move'))
        elif request.method == 'GET':
            if user.move_date:
                string_date = ''
                date = str(user.move_date).split(' ')[0].split('-')
                string_date += date[1]
                string_date += '/'
                string_date += date[2]
                string_date += '/'
                string_date += date[0]
                form.move_date.data = string_date
                form.street_address.data = user.future_street_address
                form.city.data = user.future_city
                form.state.data = user.future_state
                form.zip_code.data = user.future_zip_code
    else:
        return redirect(url_for('create_move'))  
    return render_template('edit_move.html', title='Edit Move',form=form)
################################ DONE THIS FUNCTION ##########################################

################################ DONE THIS FUNCTION ##########################################
@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html',title='Edit Profile', form=form)
################################ DONE THIS FUNCTION ##########################################

