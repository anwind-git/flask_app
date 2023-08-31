from flask import Flask, render_template, request, redirect, make_response
import utils
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    title = utils.menu_header[0]['title']
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Создание cookie-файла
        settings = make_response(redirect('/welcome'))
        settings.set_cookie('name', name)
        settings.set_cookie('email', email)
        return settings
    return render_template("index.html", settings=utils, title=title)


@app.route('/welcome')
def welcome():
    # Получение данных из cookie-файла
    title = request.cookies.get('name')
    email = request.cookies.get('email')
    return render_template('welcome.html', name=title, email=email, settings=utils, title=title)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Удаление cookie-файла
    response = make_response(redirect('/'))
    response.delete_cookie('name')
    response.delete_cookie('email')
    return response


@app.route('/<string:slug>')
def index_categories(slug):
    for link in utils.categories:
        if link['slug'] == slug:
            return render_template("index.html", settings=utils, title=f"категория товара: {link['name'].lower()}")
    return "404 - Page not found"


@app.route('/contacts')
def contacts():
    title = utils.menu_header[1]['title']
    return render_template("contacts.html", settings=utils, title=title)


@app.route('/privacy-policy')
def privacy_policy():
    title = utils.menu_footer[0]['title']
    return render_template("privacy-policy.html", settings=utils, title=title)


@app.route('/user-agreement')
def user_agreement():
    title = utils.menu_footer[1]['title']
    return render_template("user-agreement.html", settings=utils, title=title)


if __name__ == "__main__":
    app.run(debug=True)