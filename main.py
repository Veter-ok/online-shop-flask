from flask import Flask, render_template, redirect, url_for
from data import db_session
from data.users import User
from forms import SingUpForm, LoginForm

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
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user is not None:
            return redirect(url_for('profile', userID=user.id))
    return render_template("login.html", form=form)

@app.route('/singup', methods=['POST', 'GET'])
def singup():
    form = SingUpForm()
    if form.validate_on_submit():
        new_user = User(username=form.name.data, email=form.email.data, password=form.password.data)
        db_sess.add(new_user)
        db_sess.commit()
        return redirect(url_for('login'))
    return render_template("singup.html", form=form)

@app.route('/success')
def success():
    return render_template("home.html")

@app.route('/profile/<userID>')
def profile(userID):
    user = db_sess.query(User).filter(User.id == userID).first()
    if user is not None:
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/shop')
def shop():
    return render_template('shop.html')


if __name__ == '__main__':
    with app.app_context():
        db_session.global_init('database/users.db')
    db_sess = db_session.create_session()
    app.run(debug=True)