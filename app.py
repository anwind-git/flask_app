from flask import Flask, render_template, request, redirect, session
from forms import LoginForm, RegistrationForm
from modls import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
import utils

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)

app.config['SECRET_KEY'] = b'sdsfad44jh6j54hfasddfdbbmhdhjldh11dasdsf'
csrf = CSRFProtect(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    context = {'title': utils.menu_header[0]['title']}
    return render_template("index.html", form=form, settings=utils, **context)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        new_user = User(first_name=request.form['FirstName'],
                        last_name=request.form['LastName'],
                        email=request.form['Email'],
                        password=generate_password_hash(request.form['password']))
        open_user = User.query.filter(User.email == request.form['Email']).first()
        print(open_user)
        if not open_user:
            db.session.add(new_user)
            db.session.commit()
        else:
            new_user = {'id':0, 'error_email': f'Пользователь с таким email: {open_user.email} уже существует!'}
    else:
        return redirect('/')

    return render_template('register.html',
                           form=form,
                           new_user=new_user,
                           settings=utils)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        open_user = User.query.filter(User.email == request.form['authorizationEmail']).first()
        if open_user and check_password_hash(str(open_user.password), str(request.form['authorizationPassword'])):
            open_user = {'id': open_user.id, 'last_name': open_user.last_name}
            return render_template('user.html', open_user=open_user, form=form, settings=utils)
        else:
            open_user = {'id': 0, 'error_email': 'Ошибка ввода электронной почты или пароля'}
            return render_template('user.html', open_user=open_user, form=form, settings=utils)
    return redirect('/')


@app.route('/<string:slug>')
def index_categories(slug):
    form = RegistrationForm()
    for link in utils.categories:
        if link['slug'] == slug:
            return render_template("index.html",
                                   form=form,
                                   settings=utils,
                                   title=f"категория товара: {link['name'].lower()}")
    return "404 - Page not found"


@app.route('/contacts')
def contacts():
    form = RegistrationForm()
    title = utils.menu_header[1]['title']
    return render_template("contacts.html", form=form, settings=utils, title=title)


@app.route('/privacy-policy')
def privacy_policy():
    form = RegistrationForm()
    title = utils.menu_footer[0]['title']
    return render_template("privacy-policy.html", form=form, settings=utils, title=title)


@app.route('/user-agreement')
def user_agreement():
    form = RegistrationForm()
    title = utils.menu_footer[1]['title']
    return render_template("user-agreement.html", form=form, settings=utils, title=title)


if __name__ == "__main__":
    app.run(debug=True)