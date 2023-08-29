from flask import Flask, render_template, redirect
import utils
app = Flask(__name__)


@app.route('/')
def index():
    title = utils.menu_header[0]['title']
    return render_template("index.html", settings=utils, title=title)


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