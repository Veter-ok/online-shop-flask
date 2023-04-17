from flask import Flask, render_template, redirect, url_for
from flask_login import login_user, current_user, login_required, LoginManager, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from data import db_session
from data.products import products
from data.users import User
from data.baskets import Basket
from forms import SingUpForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@app.route('/')
def home():
    return render_template('home.html', current_user=current_user)

@app.route('/about-us')
def about_us():
    return render_template('about_us.html', current_user=current_user)

@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).filter(User.id == user_id).first()

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user is not None:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('profile', userID=user.id))
    return render_template("login.html", current_user=current_user, form=form)

@app.route('/singup', methods=['POST', 'GET'])
def singup():
    form = SingUpForm()
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data, 'sha256')
        new_user = User(username=form.name.data, email=form.email.data, password=password)
        db_sess.add(new_user)
        db_sess.commit()
        return redirect(url_for('login'))
    return render_template("singup.html", current_user=current_user, form=form)

@app.route('/profile/')
@login_required
def profile():
    if current_user:
        return render_template('profile.html', user=current_user)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/basket')
@login_required
def basket():
    currnet_basket = db_sess.query(Basket).filter(Basket.id_user == current_user.id)
    total = sum([products[item.id_product]['price'] for item in currnet_basket])
    print(total)
    return render_template('basket.html', basket=currnet_basket, total=total)

@app.route('/add_to_basket/<productID>')
@login_required
def add_to_basket(productID):
    if db_sess.query(Basket).filter(Basket.id_product == productID and Basket.id_user == current_user.id).first() is None:
        product = products[int(productID)]
        new_product = Basket(id_product=int(productID), name=product['name'], description=product['description'], img=product['img'], id_user=current_user.id)
        db_sess.add(new_product)
        db_sess.commit()
    return redirect(url_for('basket'))

@app.route('/delete_to_basket/<productID>')
@login_required
def delete_to_basket(productID):
    #Basket.query.filter(Basket.id_product == productID and Basket.id_user == current_user.id).delete()
    db_sess.query(Basket).filter(Basket.id_product == productID and Basket.id_user == current_user.id).delete()
    db_sess.commit()
    return redirect(url_for('basket'))

@app.route('/shop')
def shop():
    return render_template('shop.html', current_user=current_user, products=products)


if __name__ == '__main__':
    with app.app_context():
        db_session.global_init('database/users.db')
    db_sess = db_session.create_session()
    app.run(debug=True)