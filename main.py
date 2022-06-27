from flask import Flask, redirect, render_template, request, abort, jsonify, make_response, url_for
import sqlite3
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

from data import db_session

from form.authorization_form import AuthorizationForm as AutoForm

from data.user_mod import User


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'sberbank_project_udiliya'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/', methods=['GET'])
def menu():
    q = request.args.get('q')
    if q:
        conn = sqlite3.connect('db/web.sqlite')
        cur = conn.cursor()

        cur.execute(f"""SELECT * FROM users where location='{q}'
                            ORDER BY reit""")

        one_result = cur.fetchall()
        one_result.reverse()
    else:
        conn = sqlite3.connect('db/web.sqlite')
        cur = conn.cursor()

        cur.execute("""SELECT * FROM users
                                ORDER BY reit""")

        one_result = cur.fetchall()
        one_result.reverse()
    return render_template('menu.html',
                           users=one_result,
                           location='Россия')


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    form = AutoForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email_f.data and User.id == form.id_f.data).first()
        if user:
            login_user(user)
            return redirect('/account')
        else:
            return render_template("sign_up.html",
                                   form=form,
                                   title='Авторизация',
                                   message='неправильный ID или email')
    return render_template("sign_up.html",
                           form=form,
                           title='Авторизация')


@app.route('/account', methods=['GET', 'POST'])
def account():
    if current_user.is_authenticated:
        loc = current_user.location
        reit = current_user.reit
        name = current_user.name + " " + current_user.surname
        db_sess = db_session.create_session()
        place_country = len(db_sess.query(User).filter(User.reit > reit).all())
        us = db_sess.query(User).filter(User.location == loc).all()
        place = 0
        for i in us:
            if i.reit > reit:
                place += 1
        s = len(db_sess.query(User).all())
        s_l = len(db_sess.query(User).filter(User.location == loc).all())
        return render_template('account.html',
                               location=loc,
                               reit=reit,
                               place_country=place_country,
                               s=s,
                               place=place,
                               s_l=s_l,
                               name=name)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


def main():
    db_session.global_init('db/web.sqlite')
    app.run(port=9502)


if __name__ == '__main__':
    main()