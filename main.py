from flask import Flask, render_template, redirect, url_for
from forms import MyForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

users = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about-us')
def about_us():
    return render_template('about_us.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = MyForm()
    if form.validate_on_submit():
        users.append(form.name.data)
        print(users)
        return redirect(url_for('success'))
    return render_template("login.html", form=form)

@app.route('/success')
def success():
    return render_template("home.html")

@app.route('/profile/<name>')
def profile(name):
    if name in users:
        return render_template('profile.html', name=name)
    else:
        return redirect(url_for('login'))

@app.route('/shop')
def shop():
    return render_template('shop.html')


if __name__ == '__main__':
    app.run(debug=True)