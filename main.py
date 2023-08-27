from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from recommender import recommender
from movie_details import get_movie_details

app = Flask(__name__)
app.config["SECRET_KEY"] = "appkey123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///userdetails.db"
db = SQLAlchemy(app)

islogged = False


class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    movies = db.Column(db.Text)


def check(email):
    user = UserData.query.filter_by(email=email).first()
    if user:
        return user
    else:
        return False


@app.route("/", methods=["GET", "POST"])
def home():
    global islogged
    return render_template("index.html", islogged=islogged, session=session)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        email = request.form.get("email")
        password = request.form.get("password")
        user = check(email)
        if user:
            return render_template("registration_form.html", message="Email error")
        else:
            if len(password) < 8:
                return render_template("registration_form.html", message="Password error")
            userdata = UserData(
                first_name=first_name, last_name=last_name, email=email, password=password)
            db.session.add(userdata)
            db.session.commit()
            return redirect(url_for("login", message="Registration Success"))
    return render_template("registration_form.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    global islogged
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = check(email)
        if user:
            session["firstname"] = user.first_name
            session["lastname"] = user.last_name
            session["email"] = user.email
            print(session)
            if password == user.password:
                islogged = True
                return redirect(url_for("home"))
            else:
                return render_template('login.html', message="Password error")
        else:
            return render_template("login.html", message="Email error")
    if request.method == "GET":
        message = request.args.get("message")
        if message == "Registration Success":
            return render_template("login.html", message="Registration Success")
        return render_template("login.html", message="No Error")


@app.route("/logout")
def logout():
    global islogged
    islogged = False
    session.clear()
    return redirect("/")


@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    if request.method == "GET":
        if islogged:
            movie = request.args.get("movie")
            if movie:
                recommendations, searched_movie = recommender(movie)
                session["movie"] = searched_movie
                if isinstance(recommendations, list):
                    session["movie_details"] = get_movie_details(
                        session["movie"])
                return render_template("recommend.html", session=session, recommendations=recommendations)
            return render_template("recommend.html", session=session)
        return redirect("/")
    if request.method == "POST":
        movie_name = request.form.get("movieName")
        print(movie_name)
        return redirect(url_for("recommend", movie=movie_name))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
        if True:
            pass
