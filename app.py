from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash, make_response
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from database_setup import Base, User, Genre, Book
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DBAPIError


from pprint import pprint
import httplib2
import random
import string
import json
import requests


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///library.db',
                       connect_args={'check_same_thread': False})

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create new user.
def create_user(login_session):
    """Crate a new user.
    Argument:
    login_session (dict): The login session.
    """

    new_user = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture']
    )
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_info(user_id):
    """Get user information by ID.
    Argument:
        user_id (int): The user ID.
    Returns:
        The user's details.
    """

    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    """Get user ID by email.
    Argument:
        email (str) : the email of the user.
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        DBAPIError('Error!', email, get_user_id, code=None)
        return None


# Home page.
@app.route('/')
@app.route('/genre/')
def home():
    """Go to homepage."""
    genre = session.query(Genre).all()
    books = session.query(Book).all()
    return render_template(
        'index.html', genre=genre, books=books)


# Create anti-forgery state token
@app.route('/login/')
def login():
    """Route to the login page and create anti-forgery state token."""

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template("login.html", STATE=state)


# Connect to the Google Sign-in oAuth method.
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    google_id = credentials.id_token['sub']
    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_google_id = login_session.get('google_id')
    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['google_id'] = google_id

    # Get user info.
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if the user exists. If it doesn't, make a new one.
    user_id = get_user_id(data["email"])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    # Show a welcome screen upon successful login.
    output = ''
    output += '<h2>Welcome, '
    output += login_session['username']
    output += '!</h2>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; '
    output += 'border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    flash("You are now logged in as %s!" % login_session['username'])
    print("Logged in!")
    return output


# Disconnect Google Account.
def gdisconnect():
    """Disconnect the Google account of the current logged-in user."""

    # Only disconnect the connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# Log out the currently connected user.
@app.route('/logout')
def logout():
    """Log out the currently connected user."""

    if 'username' in login_session:
        gdisconnect()
        del login_session['google_id']
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        flash("You have been successfully logged out!")
        return redirect(url_for('home'))
    else:
        flash("You were not logged in!")
        return redirect(url_for('home'))


# Add a new category.
@app.route("/catalog/genre/new/", methods=['GET', 'POST'])
def add_genre():
    """Add a new category."""

    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        if request.form['new-genre-name'] == '':
            flash('The field cannot be empty.')
            return redirect(url_for('home'))

        genre = session.query(Genre).\
            filter_by(name=request.form['new-genre-name']).first()
        if genre is not None:
            flash('The entered genre already exists.')
            return redirect(url_for('add_genre'))

        new_genre = Genre(
            name=request.form['new-genre-name'],
            user_id=login_session['user_id'])
        session.add(new_genre)
        session.commit()
        flash('New genre %s successfully created!' % new_genre.name)
        return redirect(url_for('home'))
    else:
        return render_template('new-genre.html')


# Create a new item.
@app.route("/catalog/book/new/", methods=['GET', 'POST'])
def add_book():
    """Create a new item.
    Note: This route will list all the categories that the
    logged-in user has created. There is another module called
    `add_item_by_category()` which creates items based on the
    endpoint of the category mentioned.
    """

    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        # Check if the item already exists in the database.
        # If it does, display an error.
        book = session.query(Book).filter_by(name=request.form['name']).first()
        if book:
            if book.name == request.form['name']:
                flash('The book already exists in the database!')
                return redirect(url_for("add_book"))
        new_book = Book(
            name=request.form['name'],
            genre_id=request.form['genre'],
            description=request.form['description'],
            user_id=login_session['user_id']
        )
        session.add(new_book)
        session.commit()
        flash('New book successfully created!')
        return redirect(url_for('home'))
    else:
        books = session.query(Book).\
                filter_by(user_id=login_session['user_id']).all()
        genre = session.query(Genre).all()
        return render_template(
            'new-book.html',
            books=books,
            genre=genre
        )


# Create new item by Category ID.
@app.route("/catalog/genre/<int:genre_id>/book/new/",
           methods=['GET', 'POST'])
def add_book_by_genre(genre_id):
    """Create new item by Category ID."""

    if 'username' not in login_session:
        flash("You were not authorised to access that page.")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        # Check if the item already exists in the database.
        # If it does, display an error.
        book = session.query(Book).filter_by(name=request.form['name']).first()
        if book:
            if book.name == request.form['name']:
                flash('The item already exists in the database!')
                return redirect(url_for("add_book"))
        new_book = Book(
            name=request.form['name'],
            genre_id=genre_id,
            description=request.form['description'],
            user_id=login_session['user_id'])
        session.add(new_book)
        session.commit()
        flash('New book successfully created!')
        return redirect(url_for('show_books_in_genre',
                                genre_id=genre_id))
    else:
        genre = session.query(Genre).filter_by(id=genre_id).first()
        return render_template('new-book-2.html', genre=genre)


# Check if the item exists in the database,
def exists_book(book_id):
    """Check if the item exists in the database.
    Argument:
        item_id (int) : The item ID to find in the database.
    Returns:
        A boolean value indicating whether the item exists or not.
    """

    book = session.query(Book).filter_by(id=book_id).first()
    if book is not None:
        return True
    else:
        return False


# Check if the category exists in the database.
def exists_genre(genre_id):
    """Check if the category exists in the database.
    Argument:
        category_id (int) : The Category ID to find in the database.
    Returns:
        A boolean vale indicating whether the category exists or not.
    """

    genre = session.query(Genre).filter_by(id=genre_id).first()
    if genre is not None:
        return True
    else:
        return False


# View an item by its ID.
@app.route('/genre/book/<int:book_id>/')
def view_book(book_id):
    """View an item by its ID."""

    if exists_book(book_id):
        book = session.query(Book).filter_by(id=book_id).first()
        genre = session.query(Genre)\
            .filter_by(id=book.genre_id).first()
        owner = session.query(User).filter_by(id=book.user_id).first()
        return render_template(
            "view-book.html",
            book=book,
            genre=genre,
            owner=owner
        )
    else:
        flash('We are unable to process your request right now.')
        return redirect(url_for('home'))


# Edit existing item.
@app.route("/genre/book/<int:book_id>/edit/", methods=['GET', 'POST'])
def edit_book(book_id):
    """Edit existing item."""

    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('login'))

    if not exists_book(book_id):
        flash("We are unable to process your request right now.")
        return redirect(url_for('home'))

    book = session.query(Book).filter_by(id=book_id).first()
    if login_session['user_id'] != book.user_id:
        flash("You were not authorised to access that page.")
        return redirect(url_for('home'))

    if request.method == 'POST':
        if request.form['name']:
            book.name = request.form['name']
        if request.form['description']:
            book.description = request.form['description']
        if request.form['genre']:
            book.genre_id = request.form['genre']
        session.add(book)
        session.commit()
        flash('Item successfully updated!')
        return redirect(url_for('edit_book', book_id=book_id))
    else:
        genre = session.query(Genre).\
            filter_by(user_id=login_session['user_id']).all()
        return render_template(
            'update-book.html',
            book=book,
            genre=genre
        )


# Delete existing item.
@app.route("/genre/book/<int:book_id>/delete/", methods=['GET', 'POST'])
def delete_book(book_id):
    """Delete existing item."""

    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('login'))

    if not exists_book(book_id):
        flash("We are unable to process your request right now.")
        return redirect(url_for('home'))

    book = session.query(Book).filter_by(id=book_id).first()
    if login_session['user_id'] != book.user_id:
        flash("You were not authorised to access that page.")
        return redirect(url_for('home'))

    if request.method == 'POST':
        session.delete(book)
        session.commit()
        flash("Item successfully deleted!")
        return redirect(url_for('home'))
    else:
        return render_template('delete.html', book=book)


# Show items in a particular category.
@app.route('/catalog/genre/<int:genre_id>/books/')
def show_books_in_genre(genre_id):
    """# Show items in a particular category."""

    if not exists_genre(genre_id):
        flash("We are unable to process your request right now.")
        return redirect(url_for('home'))

    genre = session.query(Genre).filter_by(id=genre_id).first()
    books = session.query(Book).filter_by(genre_id=genre.id).all()
    total = session.query(Book).filter_by(genre_id=genre.id).count()
    return render_template(
        'books.html',
        genre=genre,
        books=books,
        total=total)


# Edit a category.
@app.route('/catalog/genre/<int:genre_id>/edit/',
           methods=['GET', 'POST'])
def edit_genre(genre_id):
    """Edit a category."""

    genre = session.query(Genre).filter_by(id=genre_id).first()

    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('login'))

    if not exists_genre(genre_id):
        flash("We are unable to process your request right now.")
        return redirect(url_for('home'))

    # If the logged in user does not have authorisation to
    # edit the category, redirect to homepage.
    if login_session['user_id'] != genre.user_id:
        flash("We are unable to process your request right now.")
        return redirect(url_for('home'))

    if request.method == 'POST':
        if request.form['name']:
            genre.name = request.form['name']
            session.add(genre)
            session.commit()
            flash('Genre successfully updated!')
            return redirect(url_for('show_books_in_genre',
                                    genre_id=genre.id))
    else:
        return render_template('edit_genre.html', genre=genre)


# Delete a category.
@app.route('/catalog/genre/<int:genre_id>/delete/',
           methods=['GET', 'POST'])
def delete_genre(genre_id):
    """Delete a category."""

    genre = session.query(Genre).filter_by(id=genre_id).first()

    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('login'))

    if not exists_genre(genre_id):
        flash("We are unable to process your request right now.")
        return redirect(url_for('home'))

    # If the logged in user does not have authorisation to
    # edit the category, redirect to homepage.
    if login_session['user_id'] != genre.user_id:
        flash("We are unable to process your request right now.")
        return redirect(url_for('home'))

    if request.method == 'POST':
        session.delete(genre)
        session.commit()
        flash("Genre successfully deleted!")
        return redirect(url_for('home'))
    else:
        return render_template("delete_genre.html", genre=genre)


# JSON Endpoints

# Return JSON of all the items in the catalog.
@app.route('/api/v1/genre/JSON')
def show_catalog_json():
    """Return JSON of all the items in the catalog."""

    books = session.query(Book).order_by(Book.id.desc())
    return jsonify(genre=[i.serialize for i in books])


# Return JSON of a particular item in the catalog.
@app.route(
    '/api/v1/genre/<int:genre_id>/book/<int:book_id>/JSON')
def catalog_book_json(genre_id, book_id):
    """Return JSON of a particular item in the catalog."""

    if exists_genre(genre_id) and exists_book(book_id):
        book = session.query(Book)\
                .filter_by(id=book_id, genre_id=genre_id).first()
        if book is not None:
            return jsonify(item=book.serialize)
        else:
            return jsonify(
                error='book {} does not belong to genre {}.'
                .format(book_id, genre_id))
    else:
        return jsonify(error='The book or the genre does not exist.')


# Return JSON of a all items in the catalog.
@app.route(
    '/api/v1/genre/<int:genre_id>/books/JSON')
def catalog_books_list_json(genre_id):
    """Return JSON of a particular item in the catalog."""

    if exists_genre(genre_id):
        books = session.query(Book)\
                .filter_by(genre_id=genre_id).all()
        if books is not None:
            return jsonify(item=[i.serialize for i in books])
        else:
            return jsonify(
                error='genre {} does not contain any books.'
                .format(genre_id))
    else:
        return jsonify(error='The genre does not exist.')


# Return JSON of all the categories in the catalog.
@app.route('/api/v1/genre/JSON')
def categories_json():
    """Returns JSON of all the categories in the catalog."""

    genre = session.query(Genre).all()
    return jsonify(genre=[i.serialize for i in genre])


if __name__ == "__main__":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(host="0.0.0.0", port=5000, debug=True)
